# TODO(st9_8) Update comments to be more explicit

from sys import exit

from njembe import VERSION
from njembe.utils import generate_docfile
from njembe.models import Documentation, Step, db
from njembe.config import LOG_FILE, WORKING_FILE, EXPORT_FOLDER, EDITOR

import os
import click
import logging
import datetime

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
@click.version_option(VERSION)
def njembe():
	"""
		A simple tool to help us to document our strong command line processes
	"""
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
	if EDITOR:
		os.system(f'{EDITOR} {WORKING_FILE}')
	else:
		os.system(f'editor {WORKING_FILE}')
		logging.error('env variable $EDITOR doesn\'t exist, set it to your favorite editor')

	if os.path.exists(WORKING_FILE):
		with open(WORKING_FILE) as tmp:
			step.description = tmp.read()
		os.remove(WORKING_FILE)

	step.save()
	documentation.steps += 1
	documentation.save()

@njembe.command('list')
def show_projects():
	"""
		Show all availables documentation projects.
	"""
	projects = Documentation.select()

	for project in projects:
		click.echo(f'{project.id}: {project.title} [{"Closed" if project.closed else "Open"}]')


@njembe.command('export', context_settings=CONTEXT_SETTINGS)
@click.option('-b', '--bash/--no-bash', default=False, help='Export documentation file as executable bash script.')
@click.pass_context
def export_project(ctx, bash):
	"""
		Export a specific documentation in njembe folder.
	"""
	ctx.invoke(show_projects)
	
	try:
		doc_id = int(input('Enter the documentation ID: '))

		documentation = Documentation.get_by_id(doc_id)
		steps = Step.select().where(Step.documentation==doc_id).order_by(Step.position.asc())
		
		generate_docfile(documentation, steps, bash=bash)
	except ValueError:
		click.echo('Wrong value')
		return
	except Documentation.DoesNotExist:
		click.echo('This documentation doesn\'t exist')


if __name__ == "__main__":
	# Create data folder
	from pathlib import Path
	
	export_path = Path(EXPORT_FOLDER)
	if not export_path.exists():
		export_path.mkdir(parents=True)
		(export_path / "logs").mkdir(parents=True)
		db.create_tables([Documentation, Step])

	if not (export_path / "generated_docs").exists():
		(export_path / "generated_docs").mkdir(parents=True)

	if not (export_path / "generated_scripts").exists():
		(export_path / "generated_scripts").mkdir(parents=True)		

	logging.basicConfig(filename=LOG_FILE, level=logging.ERROR,
                        format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	njembe(prog_name='njembe')
