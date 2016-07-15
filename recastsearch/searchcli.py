import click


@click.group()
def start():
    pass

@frontendcli.command()
@click.option('--config', '-c')
def main(config):
    pass

@frontendcli.command()
@click.option('--config', '-c')
def clear(config):
    pass


@frontendcli.command()
@click.opton('--config', '-c')
def dump(config):
    pass


@frontendcli.command()
@click.option('--config', '-c')
def fill(config):
    #quick fill and exits
    pass
