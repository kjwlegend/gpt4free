import sys
from . import Provider
from g4f import models

logging = False

class ChatCompletion:
    @staticmethod
    def create(model: models.Model or str, messages: list, provider: Provider.Provider = None, stream: bool = False, auth: str = False, **kwargs):
        kwargs['auth'] = auth
        if provider and provider.working == False:
            return f'{provider.__name__} is not working'

        if provider and provider.needs_auth and not auth:
            print(
                f'ValueError: {provider.__name__} requires authentication (use auth="cookie or token or jwt ..." param)', file=sys.stderr)
            sys.exit(1)

        try:
            if isinstance(model, str):
                try:
                    model = models.ModelUtils.convert[model]
                except KeyError:
                    raise Exception(f'The model: {model} does not exist')

            engine = model.best_provider if not provider else provider

            if not engine.supports_stream and stream == True:
                print(
                    f"ValueError: {engine.__name__} does not support 'stream' argument", file=sys.stderr)
                sys.exit(1)

            if logging: print(f'Using {engine.__name__} provider')

            return (engine._create_completion(model.name, messages, stream, **kwargs)
                    if stream else ''.join(engine._create_completion(model.name, messages, stream, **kwargs)))
        except TypeError as e:
            print(e)
            arg: str = str(e).split("'")[1]
            print(
                f"ValueError: {engine.__name__} does not support '{arg}' argument", file=sys.stderr)
            sys.exit(1)