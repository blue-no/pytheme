from __future__ import annotations

from pathlib import Path
from typing import Any

import click

from .schedule import run_scheduling
from .theme import ColorMode, Personalization, parse_themes
from .utils import read_config


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: Any) -> None:
    config = read_config(fp=ctx.obj["fp"])
    ctx.obj["config"] = config
    if ctx.invoked_subcommand is None:
        click.echo("Running scheduling...")
        run_scheduling(config=config)


@click.group()
@click.pass_context
def theme(ctx: Any) -> None:
    pass


@theme.command()
@click.pass_context
def list(ctx: Any) -> None:
    theme_dict = parse_themes(theme_list=ctx.obj["config"]["themes"])
    for name in theme_dict.keys():
        click.echo(name)


@theme.command()
@click.argument("name", type=str)
@click.pass_context
def use(ctx: Any, name: str) -> None:
    theme_dict = parse_themes(theme_list=ctx.obj["config"]["themes"])
    try:
        theme = theme_dict[name]
    except KeyError as e:
        raise click.BadParameter(e, param_hint="name")
    mode_ = theme.mode
    if mode_ is not None:
        Personalization().apply_colormode(mode=ColorMode(mode_))
    wp_ = theme.wp
    if wp_ is not None:
        Personalization().apply_wallpaper(wp=Path(wp_))


def main(config_fp: Path) -> None:
    obj = {"fp": config_fp}
    cli.add_command(theme)
    cli(obj=obj)
