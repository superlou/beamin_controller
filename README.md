# Beamin Controller

This is intended to be used with the Beamin target for managing Info-Beamer instances running on many systems.  It is currently only compatible with Python 3.  Use pip/pip3 to install.

## Beamin Commands

The command line interface is available by running `beamin --help`.  To display a real-time status board, run `beamin_status`.

## Configuration

All commands require a `config.json` file in the current directory.

```json
{
  "targets": [
    {
      "location": "127.0.0.1"
    },
    {
      "location": "raspberrypi"
    }
  ],
  "node_root": "~/workspace/next-beamer",
  "push_groups": [
    {
      "name": "default",
      "include": "data_*.json",
      "exclude": "data_slides.json"
    },
    {
      "name": "all",
      "include": "*"
    }
  ]
}
```

The `targets` list defines the systems hosting Info-Beamer with a location that is either the hostname or IP address.

## Controlling Targets

Targets may be started and stopped using the `--start` and `--stop` commands.

## Pushing Data

The `node_root` and `push_groups` are used to control sending updates to the targets.

The `node_root` must point to the directory containing your Info-Beamer node.  This may include a `~` which will be expanded to the current user's home.

Each push group must specify the pattern of files it includes, and, optionally, the patterns that are excluded.  An array of patterns may be passed to either.

The `push_groups` define what data will be sent using the `--push` command:

```bash
$ beamin --push       # Send the default group
$ beamin --push all   # Send the data in the group named all
```

Multiple groups may be specified in the same push command.
