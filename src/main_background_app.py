from main import background_app


if __name__ == "__main__":

    argv = [
        'worker',
        '--loglevel=DEBUG',
    ]
    background_app.worker_main(argv)