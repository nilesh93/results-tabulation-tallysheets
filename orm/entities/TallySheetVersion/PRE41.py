from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import HistoryVersion, TallySheetVersion
from orm.entities.Result import PartyWiseResult


class TallySheetVersionPRE41Model(db.Model):
    __tablename__ = 'tallySheetVersion_PRE41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                    primary_key=True)
    partyWiseResultId = db.Column(db.Integer, db.ForeignKey(PartyWiseResult.Model.__table__.c.partyWiseResultId))

    partyWiseResult = relationship(PartyWiseResult.Model, foreign_keys=[partyWiseResultId])
    tallySheetVersion = relationship("TallySheetVersionModel", foreign_keys=[tallySheetVersionId])

    tallySheetId = association_proxy("tallySheetVersion", "tallySheetId")
    tallySheet = association_proxy("tallySheetVersion", "tallySheet")
    historyVersion = association_proxy("tallySheetVersion", "historyVersion")
    tallySheetCode = association_proxy("tallySheetVersion", "tallySheetCode")
    createdBy = association_proxy("tallySheetVersion", "createdBy")
    createdAt = association_proxy("tallySheetVersion", "createdAt")
    # tallySheetContent = association_proxy("tallySheetVersion", "tallySheetContent")




Model = TallySheetVersionPRE41Model


def get_by_id(tallySheetVersionId):
    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    tallySheetVersion = TallySheetVersion.create(tallySheetId=tallySheetId)
    partyWiseResult = PartyWiseResult.create()

    result = Model(
        tallySheetVersionId=tallySheetVersion.tallySheetVersionId,
        partyWiseResultId=partyWiseResult.partyWiseResultId
    )
    db.session.add(result)
    db.session.commit()

    return result