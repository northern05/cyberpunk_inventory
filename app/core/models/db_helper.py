from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from app.core.config import config


class DatabaseHelper:
    """
    Database Helper Class
    ---
    description: Provides utility functions for managing database sessions.
    """
    def __init__(self, url: str, echo: bool = False):
        """
        Constructor method to initialize the DatabaseHelper class.
        ---
        description: Initializes the DatabaseHelper with the provided database URL and echo setting.
        parameters:
            - name: url
              in: body
              description: URL of the database
              required: true
              schema:
                type: string
            - name: echo
              in: body
              description: Echo setting for SQLAlchemy engine
              required: false
              schema:
                type: boolean
        """
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """
        Get Scoped Session
        ---
        description: Creates a new scoped database session.
        responses:
            200:
                description: Returns a new scoped database session.
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        Session Dependency
        ---
        description: Creates a new database session with context manager.
        responses:
            200:
                description: Returns a new database session.
        """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        """
        Scoped Session Dependency
        ---
        description: Creates a new scoped database session with context manager.
        responses:
            200:
                description: Returns a new scoped database session.
        """
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=config.SQLALCHEMY_DATABASE_URL,
    echo=config.db_echo,
)
