from dishka import make_container

from entrypoint.presentation.di.providers import ClientProvider, LogerProvider


sync_container = make_container(LogerProvider(), ClientProvider())
