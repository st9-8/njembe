# TODO(st9_8) Update comments to be more explicit

from sys import exit
from configparser import ConfigParser
from pkg_resources import resource_stream

from njembe import VERSION
from njembe.models import Documentation, Step

import os
import click
import logging
import datetime

@click.group()
@click.version_option(VERSION)
def njembe():
	pass

@njembe.command('open')
def init_doc():
	"""
		Initialize a new documentation project.
	"""
	
	query = Documentation.select().where(Documentation.closed==False)
	if query.exists():
		logging.error('Can\'t open a new documentation when another one is opened')
		exit(0)

	title = input('Enter the documentation title: ')
	documentation = Documentation.create(title=title)
	click.echo('Documentation created')

@njembe.command('close')
def close_doc():
	"""
		Close the current documentation project.
	"""
	try:
		documentation = Documentation.select().where(Documentation.closed==False).order_by(Documentation.created_date.desc()).get()
		documentation.closed = True
		documentation.save()
	except Documentation.DoesNotExist:
		logging.info('No project to close')

@njembe.command('command')
@click.argument('command', nargs=-1, required=True)
def add_step(command):
	"""
		Add a new step to the documentation.
	"""

	try:
		documentation = Documentation.select().where(Documentation.closed==False).order_by(Documentation.created_date.desc()).get()
	except Documentation.DoesNotExist:
		logging.info('Not existing documentation')
		logging.info('Creating a new documentation...')

		documentation =  Documentation.create(title='Untitled')
		documentation.save()

		logging.info('Document created')
	
	
	step = Step.create(documentation=documentation, command=' '.join(command), position=(documentation.steps + 1))
	if os.getenv('EDITOR'):
		os.system(f'{os.getenv("EDITOR")} {config["DEFAULT"]["working_file"]}')
		if os.path.exists(config['DEFAULT']['working_file']):
			with open(config['DEFAULT']['working_file']) as tmp:
				step.description = tmp.read()
			os.remove(config['DEFAULT']['working_file'])
	else:
		logging.error('env variable $EDITOR doesn\'t exist, set it to your favorite editor')
	step.save()
	documentation.steps += 1
	documentation.save()

@njembe.command('list')
def show_projects():
	"""
		Function used to show saved projects of your computer.
	"""
	projects = Documentation.select()

	for project in projects:
		click.echo(f'{project.id}: {project.title} [{"Closed" if project.closed else "Open"}]')


@njembe.command('export')
@click.pass_context
def export_project(ctx):
	"""
		Export specific documentation in a folder
	"""
	ctx.invoke(show_projects)
	
	try:
		doc_id = int(input('Enter the documentation ID: '))

		documentation = Documentation.get_by_id(doc_id)
		steps = Step.select().where(Step.documentation==doc_id).order_by(Step.position.asc())
		file_to_write = os.path.join(export_path, f'Documentation_{documentation.id}.nj')
		doc = []

		doc.append(f'Title: {documentation.title}\n')
		doc.append(f'Created at: {documentation.created_date.strftime("%d-%m-%Y, %H:%M:%S")}\n')
		doc.append(f'Steps: {documentation.steps}\n')
		doc.append(f'{"-"*30}\n\n')

		if steps:
			

			for step in steps:
				doc.append(f'Step {step.position}: {step.description}\n')
				doc.append(f'Command: {step.command}\n')
				doc.append('\n')
			doc_to_write = ''.join(doc)

			with open(file_to_write, 'w') as doc_file:
				doc_file.write(doc_to_write)
		else:
			doc.append('No steps in this documentation')
			doc_to_write = ''.join(doc)

			with open(file_to_write, 'w') as doc_file:
				doc_file.write(doc_to_write)
		click.echo(f'Documentation available at {file_to_write}')

	except ValueError:
		click.echo('Wrong value')
		return
	except Documentation.DoesNotExist:
		click.echo('This documentation doesn\'t exist')


if __name__ == "__main__":
	config = ConfigParser()
	config.read(resource_stream('njembe', 'config.ini').name)

	# Create data folder
	export_path = config['DEFAULT']['export_folder'].format(os.getenv('HOME'))

	if not os.path.exists(export_path):
		os.mkdir(export_path)
		os.mkdir(os.path.join(export_path, 'logs'))


	log_filename = config['DEFAULT']['log_file'].format(os.getenv('HOME'))

	logging.basicConfig(filename=log_filename, level=logging.ERROR,
                        format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	njembe(prog_name='njembe')
