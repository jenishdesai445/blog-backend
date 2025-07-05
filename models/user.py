from sqlalchemy import Column, Integer, ARRAY, String, Boolean, DateTime, Date, Table
from db.base_class import Base
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True)

    password = Column((String()), nullable=False)
    email = Column((String(256)), unique=True, nullable=False)
    first_name = Column((String(256)), nullable=False)
    last_name = Column((String(256)), nullable=False)
    phone = Column((String(256)), nullable=True)
    gender = Column((String(256)), nullable=True)
    created_by = Column(Integer, nullable=True)

    modified_by = Column(Integer, nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=False)
