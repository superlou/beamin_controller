# Beamin Controller

This is intended to be used with the Beamin target for managing Info-Beamer instances running on many systems.  It is currently only compatible with Python 3.  Use pip/pip3 to install.

## Run

The command line interface is available by running `beamin --help`.  To display a real-time status board, run `beamin_status`.

## Configuration

Both commands require a `targets.json` file in the current directory.  This is simply a list of systems hosting Info-Beamer with a location that is either the hostname or IP address.

```json
{
  "targets": [
    {
      "location": "127.0.0.1"
    },
    {
      "location": "raspberrypi"
    }
  ]
}
```
