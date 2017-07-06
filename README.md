# project-playbills-mark

> Playbills marking projects for LibCrowds.

Tasks are generated by choosing a set of tasks from
[src/data/tasks.json](src/data/tasks.json) (e.g. `"titles"`) and either an
Aleph system number from
[src/data/arks_and_sysnos.csv](src/data/arks_and_sysnos.csv) or a JSON file
containing the results data of a previous project-playbills-mark project. Once
these choices have been made follow the instructions below for installing,
building and deploying.

When generating tasks from an Aleph system number a task will be created
for each permutation of image and task in the chosen set. When generating
tasks from a JSON results file a task will be created for each result, each
region now associated with the result and each task in the chosen task set.
The idea being that we can chain tasks to highlight increasingly more specific
regions in the text (e.g. all actors associated with a title).

## Install

Install [Node.js](https://nodejs.org/en/) and
[Python](https://www.python.org/downloads/), then:

```
# install JavaScript dependencies
npm install
```

## Building

```
# bundle JavaScript
npm run build

# generate project files
python bin/generate.py <task set> [--sysno=<sysno> or --json=<path>]
```

## Deploying

If you haven't already done so, configure pbs according to the
[documentation](https://github.com/Scifabric/pbs#configuring-pbs), then:

```
# deploy to the server
cd dist
pbs create_project
pbs add_tasks --tasks-file=tasks.csv
pbs update-task-redundancy --redundancy 3
pbs update_project
```

Once you have updated any additional settings on the server (category,
thumbnail, webhooks etc.), the project is ready to be published.

## Developing

```
# watch for JavaScript changes
npm run dev

# auto-update on the server
cd dist
pbs update_project --watch
```

### Defining new task sets

Task sets are defined in [src/data/tasks.json](src/data/tasks.json) using the
following structure:

``` json
"taskset_name": {
  "nameSuffix": "Appended to the catalogue title to create the project title",
  "description": "A one line description of the project",
  "tasks": [
    {
      "category": "some_category",
      "objective": "The objective of the task",
      "guidance": "Additional guidance"
    }
  ]
}
```

If `guidance` is set to `null` and the task set is being generated from the
results of a previous marking project then the guidance will be generated
automatically in the form "Identify each <category> associated with the
highlighted <parent task category>.".
