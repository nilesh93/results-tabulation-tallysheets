from app import db
from sqlalchemy.orm import relationship
from orm.enums import OfficeTypeEnum
from orm.entities import Election
from sqlalchemy.ext.hybrid import hybrid_property

from util import get_paginated_query


class OfficeModel(db.Model):
    __tablename__ = 'office'
    officeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    officeName = db.Column(db.String(100), nullable=False)
    officeType = db.Column(db.Enum(OfficeTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    parentOfficeId = db.Column(db.Integer, db.ForeignKey(officeId), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    parentOffice = relationship("OfficeModel", remote_side=[officeId])
    childOffices = relationship("OfficeModel", foreign_keys=[parentOfficeId])
    # tallySheets = relationship("TallySheetModel")

    @hybrid_property
    def allPollingStations(self):
        result = []
        if self.childOffices is not None:
            for childOffice in self.childOffices:
                if childOffice.__class__.__name__ != "PollingStationModel":
                    result = result + childOffice.allPollingStations
                else:
                    result.append(childOffice)

        return result

    __mapper_args__ = {
        'polymorphic_on': officeType
    }


Model = OfficeModel


def create(officeName, officeType, electionId, parentOfficeId=None):
    result = Model(
        officeName=officeName,
        officeType=officeType,
        electionId=electionId,
        parentOfficeId=parentOfficeId
    )
    db.session.add(result)
    db.session.commit()

    return result


def get_all(electionId=None, officeName=None, parentOfficeId=None, officeType=None):
    query = Model.query

    if officeName is not None:
        query = query.filter(Model.officeName.like(officeName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if officeType is not None:
        query = query.filter(Model.officeType == officeType)
    else:
        query = query.filter(Model.parentOfficeId == parentOfficeId)

    result = get_paginated_query(query).all()

    return result
