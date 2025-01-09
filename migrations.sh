export PYTHONPATH=$PWD
# alembic -c app/libs/mysql/alembic.ini revision -m "create register table"
# alembic -c app/libs/mysql/alembic.ini upgrade head

# alembic -c app/libs/mysql/alembic.ini revision -m "add a column"
# alembic -c app/libs/mysql/alembic.ini upgrade head

# Getting Info
# alembic -c app/libs/mysql/alembic.ini current
# alembic -c app/libs/mysql/alembic.ini history --verbose

# alembic -c app/libs/mysql/alembic.ini downgrade c977e378daf0
# alembic -c app/libs/mysql/alembic.ini downgrade base

#AUTO Generating
#alembic -c app/libs/mysql/alembic.ini revision --autogenerate -m "add password_updated_at to user"
alembic -c app/libs/mysql/alembic.ini upgrade head
# alembic -c app/libs/mysql/alembic.ini downgrade base