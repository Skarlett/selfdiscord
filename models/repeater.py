import time
from ._base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

class AdvertisementSchema(Base):
  uuid = Column(Integer, autoincrement=True, primary_key=True)
  content = Column(String(2000), index=True)
  lang = Column(String(16), default='EN')
  created_at = Column(Integer, default=time.time())
  ads = relationship("Advertisement", uselist=True, backref="ad")


class Advertisement(Base):
  uuid = Column(Integer, autoincrement=True, primary_key=True)
  channel = Column(Integer) != None
  created_at = Column(Integer, default=time.time())
  target_lang = Column(String(16), default="EN")
  source = Column(Integer, ForeignKey('advertisementschema.uuid')) != None
  meta = relationship("AdvertisementMeta", uselist=False, backref="ad")
  

class AdvertisementMeta(Base):
  uuid = Column(Integer, autoincrement=True, primary_key=True)
  repeater = Column(Integer, default=3600)
  active = Column(Boolean, default=False)
  hits = Column(Integer, default=0)
  timestamped = Column(Integer, default=0)
  ad = Column(Integer, ForeignKey('advertisement.uuid'))
