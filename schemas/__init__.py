from app import db, ma
from orm.entities import StationaryItem, Ballot, File, Invoice, BallotBox, \
    InvoiceStationaryItem, Election, Proof, History, Submission, Electorate, SubmissionVersion
from orm.entities import TallySheet, TallySheetVersion
from orm.entities.Result import PartyWiseResult
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.enums import StationaryItemTypeEnum, ProofTypeEnum, TallySheetCodeEnum, OfficeTypeEnum, ReportCodeEnum, \
    SubmissionTypeEnum, ElectorateTypeEnum

from marshmallow_enum import EnumField


class File_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "fileId",
            "fileName",
            "fileMimeType",
            "fileContentLength",
            "fileCreatedBy",
            "fileCreatedAt",
            "urlInline",
            "urlDownload"
        )

        model = File.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class ElectionSchema(ma.ModelSchema):
    class Meta:
        model = Election.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class PartyCountSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "partyId",
            "count",
            "countInWords"
        )

        model = PartyCount.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            # "electionId",
            # "officeId",
            # "latestVersionId",

            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "tallySheetContent"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    tallySheetCode = EnumField(TallySheetCodeEnum)
    tallySheetContent = ma.Nested(PartyCountSchema, many=True)


class ElectorateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "electorateId",
            "electorateName",
            "electorateType",
            "electionId",
            "parentelectorate"
        )

        model = Electorate.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    electorateType = EnumField(ElectorateTypeEnum)
    parentelectorate = ma.Nested('self')


class OfficeSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "officeId",
            "officeName",
            "officeType",
            "electionId",
            "parentOffice"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    officeType = EnumField(OfficeTypeEnum)
    parentOffice = ma.Nested('self')


class Proof_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "proofId",
            "proofType",
            "finished",
            "scannedFiles"
        )

        model = Proof.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    scannedFiles = ma.Nested(File_Schema, many=True)
    proofType = EnumField(ProofTypeEnum)


class SubmissionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "submissionId",
            "submissionType",
            "electionId",
            "office",
            "electorate",
            "latestVersionId",
            # "tallySheetProofId",
            "parentSubmission",
            "childSubmissions",
            "submissionProofId",
            "versions"
        )

        model = Submission.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # latestVersion = ma.Nested(TallySheetVersionSchema)
    office = ma.Nested(OfficeSchema)
    electorate = ma.Nested(ElectorateSchema)
    submissionType = EnumField(SubmissionTypeEnum)
    submissionProof = ma.Nested(Proof_Schema)


class SubmissionVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "submissionVersionId",
            # "submission",
            "createdBy",
            "createdAt"
        )

        model = SubmissionVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    submission = EnumField(SubmissionSchema)


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "submissionVersionId",
            "submission",
            "createdBy",
            "createdAt"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    submission = EnumField(SubmissionSchema)


class ReportVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "reportId",
            "reportVersionId",
            "createdBy",
            "createdAt",
            "reportFile"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    reportFile = ma.Nested(File_Schema)

class TallySheetVersionPRE41Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "tallySheetContent"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    tallySheetContent = ma.Nested(PartyCountSchema, many=True)


class TallySheetSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            "electionId",
            "office",
            "electorate",
            "latestVersionId",
            "parentSubmission",
            "childSubmissions",
            "submissionProofId",
            "versions"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    tallySheetCode = EnumField(TallySheetCodeEnum)
    # submission = ma.Nested(SubmissionSchema)
    office = ma.Nested(OfficeSchema)
    versions = ma.Nested(SubmissionVersionSchema, only="submissionVersionId", many=True)
    # versions = ma.Nested(SubmissionVersionSchema, "submissionVersionId", many=True)
    electorate = ma.Nested(ElectorateSchema)
    submissionProof = ma.Nested(Proof_Schema)


class ReportSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "reportId",
            "reportCode",
            "submission"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    reportCode = EnumField(ReportCodeEnum)
    submission = ma.Nested(SubmissionSchema)


# class TallySheet_PRE_41__party_Schema(ma.ModelSchema):
#     class Meta:
#         fields = ("partyId", "voteCount")
#
#         model = TallySheetPRE41Party.Model
#         # optionally attach a Session
#         # to use for deserialization
#         sqla_session = db.session


# class TallySheet_PRE_41_Schema(ma.ModelSchema):
#     class Meta:
#         fields = (
#             "tallySheetId",
#             "tallySheetCode",
#             "electionId",
#             "officeId",
#             "latestVersionId",
#
#             "tallySheetVersionId",
#             "createdBy",
#             "createdAt",
#
#             "electoralDistrictId",
#             "pollingDivisionId",
#             "countingCentreId",
#             "party_wise_results",
#         )
#
#         model = TallySheetPRE41.Model
#         # optionally attach a Session
#         # to use for deserialization
#         sqla_session = db.session
#
#     createdBy = ma.Integer()
#     createdAt = ma.String()
#
#     party_wise_results = ma.Nested(TallySheet_PRE_41__party_Schema, many=True)


class StationaryItem_Schema(ma.ModelSchema):
    stationaryItemType = EnumField(StationaryItemTypeEnum)

    class Meta:
        fields = (
            "stationaryItemId",
            "stationaryItemType",
            "electionId",
            "locked"
        )

        model = StationaryItem.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Invoice_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "invoiceId",
            "electionId",
            "issuingOfficeId",
            "receivingOfficeId",
            "issuedBy",
            "issuedTo",
            "issuedAt",
            "confirmed",
            "delete"
        )

        model = Invoice.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Invoice_StationaryItem_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "received",
            "receivedBy",
            "receivedFrom",
            "receivedOfficeId",
            "receivedAt",
            # "receivedProofId",
            "invoiceId",
            "stationaryItemId",
            "stationaryItem",
            "delete",
            "receivedProof"
        )

        model = InvoiceStationaryItem.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    invoice = ma.Nested(Invoice_Schema)
    stationaryItem = ma.Nested(StationaryItem_Schema)
    receivedProof = ma.Nested(Proof_Schema)


class Ballot_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotId",
            "electionId",
            "stationaryItemId",
            "stationaryItem"
        )

        model = Ballot.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    stationaryItem = ma.Nested(StationaryItem_Schema)


class BallotBox_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotBoxId",
            "electionId",
            "stationaryItemId",
            "stationaryItem"
        )

        model = BallotBox.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    stationaryItem = ma.Nested(StationaryItem_Schema)
