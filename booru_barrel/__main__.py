import argparse
import logging
import getpass
from pprint import pprint
from booru_barrel.cfg import Config
from booru_barrel.core import Runner

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='booru_barrel', description='cli + gui tool for downloading images from image boards. gui is still under construction please use cli')
    parser.set_defaults(cli=False, cfg=False, v=False)
    sub_parsers = parser.add_subparsers()

    cfg_parser = sub_parsers.add_parser('config', help='settings wizard; will create settings file for user')
    cfg_parser.set_defaults(cfg=True, list=False)
    cfg_parser.add_argument('--list', action='store_true', help='list availible sources')
    cfg_parser.add_argument('--print', action='store_true', help='print config dictionary')

    cli_parser = sub_parsers.add_parser('cli', help='use the cli instead of the gui')
    cli_parser.set_defaults(cli=True)
    cli_parser.add_argument('-s', '--source', type=str, help='source in config to query images from; will use default source if not specified')
    cli_parser.add_argument('-t', '--tags', action='append', type=str, default=[], help='search tags; use -t=\'tag\' for each tag')
    cli_parser.add_argument('-m', '--max', type=int, help='maximum number of images; will not exceed this limit')
    cli_parser.add_argument('-w', '--wait', type=float, help='seconds to sleep between requests')

    ex_cli = cli_parser.add_mutually_exclusive_group()
    ex_cli.add_argument('-o', '--output', type=str, help='output directory to save images')
    ex_cli.add_argument('-u', '--urls', action='store_true', help='print urls of images')

    log_cli = cli_parser.add_mutually_exclusive_group()
    log_cli.add_argument('-q', action='store_true', help='logs at ERROR level; makes quiet logs')
    log_cli.add_argument('-qq', action='store_true', help='logs at CRITICAL level; makes really quiet logs')
    log_cli.add_argument('-v', action='store_true', help='logs at INFO level; recomended to not use this with the --url arg')
    log_cli.add_argument('-vv', action='store_true', help='logs at DEBUG level; recomended to not use this with the --url arg')

    args = parser.parse_args()
    cfg = Config()

    if args.cli:
        if args.v:
            logging.basicConfig(level=logging.INFO)
        elif args.vv:
            logging.basicConfig(level=logging.DEBUG)
        elif args.q:
            logging.basicConfig(level=logging.ERROR)
        elif args.qq:
            logging.basicConfig(level=logging.CRITICAL)
        else:
            logging.basicConfig(level=logging.WARN)
        cfg.logger.info(args)

        runner = Runner(args.source, args.tags, args.max, args.wait, args.output)
        runner.run()

    elif args.cfg:
        if args.list:
            for src in cfg.list_sources():
                print(src)
        elif args.print:
            pprint(cfg.load_cfg())
        else:
            cfg.wizard()
            
    else:
        logging.basicConfig(level=logging.INFO)
        from booru_barrel.gui import BooruBarrelApp as app
        app().run()