from sqlalchemy import Column, String, Integer, DateTime, Float
from database import Base


class ParameterEvent(Base):

    __tablename__ = 'parameters'

    block = Column(Integer)
    timestamp = Column(DateTime)
    tx_hash = Column(String)
    source = Column(String)
    parameter = Column(String)
    ilk = Column(String)
    from_value = Column(Float)
    to_value = Column(Float)
    
    def to_dict(self):
        return {
            'block': self.block,
            'timestamp': self.timestamp.__str__()[:19], 
            'tx_hash': self.tx_hash,
            'source': self.source,
            'parameter': self.parameter,
            'ilk': self.ilk,
            'from_value': round(self.from_value, 10),
            'to_value': round(self.to_value, 10)
        }

    def to_list(self):
        return [
            self.block,
            self.timestamp.__str__()[:19], 
            self.tx_hash,
            self.source,
            self.parameter,
            self.ilk,
            round(self.from_value, 10),
            round(self.to_value, 10)
        ]
    
    __table_args__ = {"schema": "maker.public"}
    __mapper_args__ = {
        "primary_key": [
            block,
            source,
            parameter,
            ilk,
            from_value,
            to_value
        ]
    }