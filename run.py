import os
import sys
import colored
from colored import stylize
from lab.core.output import printTabs, printFullTable
from dotenv import load_dotenv
load_dotenv()


def list_commands():
    headers = ['Command', 'Description']
    print('\n')
    print('Available Subcommands')
    print('No quotes required on [<ticker>] arguments, may be typed directly into the terminal.')
    print('\n\n')

    commands = [
        ['studies:graph', 'Runs a rescaled range analysis on a ticker. Output defaults to table.'],
        ['hurst [dataset] [output=table]', 'Runs a rescaled range analysis on a ticker. Output defaults to table.'],
        ['output:last', 'Returns the last cached output, can resort by specific key.'],
        ['rdb:export', 'Exports redisdb to zipped json file'],
        ['rdb:import', 'Import redisdb from a zipped json file'],
    ]
    printTabs(commands, headers, 'simple')
    print('\n\n')


def command_error(required={}, opt=None):
    if(not (required or opt)):
        print(stylize('Error: your command did not match any known programs. Closing...', colored.fg('red')))
        print('\n')
        return

    if (required):
        print(stylize('FAILED: Requires arguments: ', colored.fg('red')))
        for var, rules in required.items():
            print(stylize('({}) [{}] in position {}'.format(rules['type'], var, rules['pos']), colored.fg('red')))
        print('\n')
    if (opt):
        print(stylize('Optional arguments: ', colored.fg('yellow')))
        if (isinstance(opt, dict)):
            for var, typ in opt.items():
                print(stylize('({}) [{}]'.format(var, typ), colored.fg('yellow')))
        if (isinstance(opt, list)):
            for var in opt.items():
                print(stylize('[{}]'.format(var), colored.fg('yellow')))
            print('\n')


def parse_args(args, required=[], opt=[]):
    params = {}

    if (required):
        for req, rules in required.items():
            if ('=' in args[rules['pos']]):
                rv = args[rules['pos']].split('=')[1]
            else:
                rv = args[rules['pos']]

            params[req] = rv

    if (required and params == {}):
        command_error()
    if (opt):
        for var, rules in opt.items():
            in_args = [var == arg.split('=')[0] for arg in args]

            if (True in in_args):
                if (rules['type'] == bool):
                    if ('--' in var):
                        var = var.split('--')[1]
                    if ('=' in var):
                        argvalue = var.split('=')[1]
                    else:
                        argvalue = True

                    params[var] = argvalue
                    continue

                argvalue = args[in_args.index(True)].split('=')[1]

                if (rules['type'] == int and isinstance(int(argvalue), int)):
                    params[var] = int(argvalue)
                    continue
                else:
                    print(stylize(var+' must be of type int.', colored.fg('red')))
                    sys.exit()

                params[var] = argvalue

    return params


def hurst_controller(args):
    required = {'dataset': {'pos': 0, 'type': str}}
    opt = {'output': {'type': str, 'default': 'table'}}

    if (not args):
        command_error(required, opt)
        return

    from lab.rescaledrange.fractal_calculator import fractal_calculator
    params = parse_args(args, required, opt)

    print(fractal_calculator(
        dataset=params['dataset'],
        output=params['output'] if ('output' in params) else opt['output']['default'],
    ))


def studies_controller(subroutine, args=[]):
    if (subroutine == 'graph'):
        from lab.studies.graph import graph_climate_data
        required = {'dataset': {'pos': 0, 'type': str}}

        if (not args):
            command_error(required)
            return

        params = parse_args(args, required)

        print(graph_climate_data(
            dataset=params['dataset']
        ))


def rdb_controller(subroutine, args=[]):
    if (subroutine == 'export'):
        from lab.redisdb.export import export_rdb
        export_rdb()
    if (subroutine == 'import'):
        from lab.redisdb.imports import import_rdb
        import_rdb()


def output_controller(subroutine, args):
    if (subroutine == 'last'):
        from lab.redisdb.controller import fetch_last_output

        results = fetch_last_output()
        printFullTable(results, struct='dictlist')
        return

    command_error()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab.settings')
    sys.argv.pop(0)

    args = [arg.strip() for arg in sys.argv]

    if (args[0] == 'list'):
        list_commands()
        return

    if (':' in args[0]):
        command = args.pop(0)
        program = command.split(':')[0] + '_controller'
        subroutine = command.split(':')[1]

        globals()[program](subroutine, args)
        return
    else:
        program = args.pop(0) + '_controller'

        globals()[program](args)
        return


if __name__ == '__main__':
    main()
