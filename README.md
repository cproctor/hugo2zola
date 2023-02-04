# Hugo2Zola

Like many others, I got tired of fighting with hugo's templating system, 
and decided to migrate to Zola. If you have a fairly large site, migration 
will be tedious. This package helps with the transition, though it probably
won't get you all the way. 

## Usage

`python h2z.py <hugo_root> <zola_root> --theme themes/easydocs --config --clean`

- `hugo_root` is the path to an existing hugo site.
- `zola_root` is a path to export the zola site. `zola_root` will be created. 
  An error will be raised if `zola_root` exists, unless `--clean` is set.
- `--theme path` is the root path to a zola theme.
- `--config` writes a stub config file to the zola site.
- `--clean` removes the export directory before migration.

## Structure

A `Migrator` walks the content tree of your old hugo site, reading content
nodes. A pipeline of `Filter`s is applied to each node's metadata and content, 
and then the node is written to your new zola site's content tree.

Filters take care of tasks such as removing or translating hugo-specific metadata, 
translating hugo syntax highlighting to zola, stripping or translating shortcodes, 
and whatever else you need to do.

You can choose to write a zola config file and copy a theme into the export 
directory, so that you can immediately serve the migrated site for testing.

Hugo and Zola are both feature-rich and open-ended, so it's doubtful that
any tool could provide full coverage for a migration. Instead, this tool 
provides a reproducible migration which you can iteratively tweak by 
configuring filters, or writing new filters. 

## Running tests

`python -m unittest discover -s tests`
