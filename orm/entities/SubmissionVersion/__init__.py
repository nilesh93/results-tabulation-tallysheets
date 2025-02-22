from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import HistoryVersion, Submission

from orm.enums import ProofTypeEnum

from exception import NotFoundException


class SubmissionVersionModel(db.Model):
    __tablename__ = 'submissionVersion'
    submissionVersionId = db.Column(db.Integer, db.ForeignKey(HistoryVersion.Model.__table__.c.historyVersionId),
                                    primary_key=True)
    submissionId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId))

    submission = relationship(Submission.Model, foreign_keys=[submissionId])
    historyVersion = relationship(HistoryVersion.Model, foreign_keys=[submissionVersionId])

    createdBy = association_proxy("historyVersion", "createdBy")
    createdAt = association_proxy("historyVersion", "createdAt")


Model = SubmissionVersionModel


def get_all(submissionId, submissionCode=None):
    query = Model.query.filter(Model.submissionId == submissionId)

    if submissionCode is not None:
        query = query.filter(Model.submissionCode == submissionCode)

    result = get_paginated_query(query).all()

    return result


def create(submissionId):
    submission = Submission.get_by_id(submissionId=submissionId)
    if submission is None:
        raise NotFoundException("Submission not found. (submissionId=%d)" % submissionId)

    historyVersion = HistoryVersion.create(submission.submissionHistoryId)

    result = Model(
        submissionId=submissionId,
        submissionVersionId=historyVersion.historyVersionId,
    )
    db.session.add(result)
    db.session.commit()

    return result
