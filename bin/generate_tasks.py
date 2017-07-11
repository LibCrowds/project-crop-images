#-*- coding: utf8 -*-
"""
A script for generating the tasks for a project-iiif-mark project.
"""
import os
import json
import argparse
import itertools
from helpers import get_task, mkdist, set_config_dir, load_json
from helpers import get_manifest
from helpers import DIST_DIR


def add_iiif_config(task_data):
    """Add IIIF config to task data."""
    iiif_json = load_json('iiif.json')
    for obj in task_data:
        obj.update(iiif_json)


def write_tasks_json(task_data):
    """Write task data to the tasks.json file."""
    path = os.path.join(DIST_DIR, 'tasks.json')
    with open(path, 'wb') as f:
        json.dump(task_data, f, indent=2)


def get_task_data_from_json(json_data, taskset):
    """Return the task data generated from JSON input data."""
    task_data = taskset['tasks']
    input_data = [{'image_id': row['info']['image_id'],
                   'manifest_url': row['info']['manifest_url'],
                   'parent_task_id': row['task_id'],
                   'region': json.dumps(region)}
                  for row in json_data
                  for region in row['info']['regions']]

    product = list(itertools.product(task_data, input_data))
    data = [dict(row[0].items() + row[1].items()) for row in product]

    # Set default guidance
    for d in data:
        if not d['guidance']:
            d['guidance'] = ("Identify each {0} associated with the "
                             "highlighted {1}.").format(d['category'],
                                                        d['parent_category'])
    return data


def get_task_data_from_manifest(category, manifest):
    """Return the task data generated from a manifest."""
    task = get_task(category)
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'] for c in canvases]
    image_arks = [img[0]['resource']['service']['@id'].split('iiif/')[1]
                  for img in images]
    data = [{
        'image_id': img_ark,
        'category': category,
        'objective': task['objective'],
        'guidance': task['guidance']
    } for img_ark in image_arks]
    return data


def generate(category, manifest_id, config=None, results=None):
    """Generate and return the tasks file."""
    mkdist()
    set_config_dir(config)
    if results:
        results_json = json.load(open(results, 'rb'))
        task_data = get_task_data_from_json(results_json, category)
    else:
        manifest = get_manifest(manifest_id)
        task_data = get_task_data_from_manifest(category, manifest)
    add_iiif_config(task_data)
    write_tasks_json(task_data)
    return task_data


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Generate tasks")
    PARSER.add_argument('category', help="A task category in tasks.json.")
    PARSER.add_argument('manifestid', help="IIIF manifest ID.")
    PARSER.add_argument('--config', help="Project configuration.")
    PARSER.add_argument('--results', help="JSON results file.")
    ARGS = PARSER.parse_args()
    DATA = generate(ARGS.category, ARGS.manifestid, ARGS.config, ARGS.results)
    print'\n{0} tasks created'.format(len(DATA))
