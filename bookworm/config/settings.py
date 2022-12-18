from pydantic import BaseSettings


class Base(BaseSettings):
    base = {
        'app_name': 'BookWorm API',
        'admin_email': 'didijc@gmail.com',
        'items_per_user': 50
    }


class Production(Base):
    super().base['environment'] = 'production'


class Development(Base):
    super().base['environment'] = 'development'


class Qa(Base):
    super().base['environment'] = 'qa'


