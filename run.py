import asyncio
import hydra
import omegaconf
from src.experiment.loader import ExperimentLoader


async def main(
    config_path="./configs", config_name="base", experiment_name="classic", overrides=[]
):
    hydra.initialize(version_base=None, config_path=config_path)
    cfg = hydra.compose(config_name=experiment_name, overrides=overrides)

    omegaconf.OmegaConf.register_new_resolver("eval", lambda s: eval(s))
    omegaconf.OmegaConf.resolve(cfg)

    experiment = ExperimentLoader.create_experiment(
        omegaconf.OmegaConf.to_container(cfg, resolve=True)
    )
    await experiment.run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default="./configs")
    parser.add_argument("--config_name", default="base")
    parser.add_argument("--experiment_name", default="debate")
    parser.add_argument("--overrides", action="append", default=[])

    asyncio.run(main(**vars(parser.parse_args())))
