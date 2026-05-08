from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .common import ModuleStatus


class VerificationModuleStatus(ModuleStatus):
    module: str = "verification"
    status: str = "contract_placeholder"
    purpose: str = "Phase 14 target ownership verification contracts, method definitions, and challenge token design."
    future_phase: str = "Phase 15 scan execution after verification"


class VerificationMethod(BaseModel):
    method: str
    label: str
    description: str
    instructions: str
    placeholder_format: str
    network_check_required: bool = False
    implemented: bool = False


class VerificationMethodRegistry(BaseModel):
    purpose: str = "Phase 14 supported verification method definitions."
    methods: List[VerificationMethod] = Field(default_factory=lambda: [
        VerificationMethod(
            method="dns_txt",
            label="DNS TXT Record",
            description="Prove domain control by adding a DNS TXT record.",
            instructions="Add a TXT record to the target domain: sherlock-verification=<challenge>. DNS propagation may take minutes to hours.",
            placeholder_format="sherlock-verification=sherlock_<token>",
            network_check_required=True,
            implemented=False,
        ),
        VerificationMethod(
            method="html_meta_tag",
            label="HTML Meta Tag",
            description="Prove control by placing a meta tag on the target homepage.",
            instructions='Add the following tag inside <head> on the target homepage: <meta name="sherlock-verification" content="<challenge>">.',
            placeholder_format='<meta name="sherlock-verification" content="sherlock_<token>">',
            network_check_required=True,
            implemented=False,
        ),
        VerificationMethod(
            method="well_known_file",
            label="Well-Known Verification File",
            description="Prove control by uploading a verification file.",
            instructions="Create the file /.well-known/sherlock-verification.txt with content: sherlock-verification=<challenge>.",
            placeholder_format="sherlock-verification=sherlock_<token>",
            network_check_required=True,
            implemented=False,
        ),
        VerificationMethod(
            method="manual_authorization",
            label="Manual Authorization Review",
            description="Submit authorization documentation for manual review.",
            instructions="Provide authorization document, legal/scope confirmation, contact person, allowed targets, testing window, and forbidden actions. An operator will review manually.",
            placeholder_format="Authorization document and scope metadata",
            network_check_required=False,
            implemented=False,
        ),
        VerificationMethod(
            method="chatbot_api_challenge",
            label="Chatbot/API Challenge",
            description="Prove API/chatbot control by returning a challenge code.",
            instructions="Sherlock sends a safe challenge message to the target: 'Return verification code exactly: <challenge>'. The target must respond with the exact challenge string.",
            placeholder_format="sherlock_<token>",
            network_check_required=True,
            implemented=False,
        ),
    ])


class VerificationStatus(BaseModel):
    status: str
    label: str
    description: str


class VerificationStatusRegistry(BaseModel):
    purpose: str = "Phase 14 verification status definitions."
    statuses: List[VerificationStatus] = Field(default_factory=lambda: [
        VerificationStatus(status="unverified", label="Unverified", description="No verification attempt has been made."),
        VerificationStatus(status="pending", label="Pending", description="A verification challenge has been created and is awaiting proof."),
        VerificationStatus(status="verified", label="Verified", description="Ownership proof was accepted. Scanning may be unlocked in a future phase."),
        VerificationStatus(status="failed", label="Failed", description="The verification check did not succeed."),
        VerificationStatus(status="expired", label="Expired", description="The challenge or verification has expired and must be retried."),
        VerificationStatus(status="manual_review_required", label="Manual Review Required", description="Manual authorization review is needed before verification can proceed."),
    ])


class ChallengeTokenDesign(BaseModel):
    purpose: str = "Phase 14 challenge token format and security boundaries."
    format: str = "sherlock_<random_urlsafe_base64_token>"
    example: str = "sherlock_aBcDeFgHiJkLmNoPqRsT"
    token_length_bytes: int = 24
    notes: List[str] = Field(default_factory=lambda: [
        "Challenge tokens are proof-of-control tokens, not secrets.",
        "Tokens should expire after a configured TTL.",
        "Tokens should be stored hashed if persisted to the database.",
        "Tokens are scoped to a specific target and verification method.",
        "Tokens do not grant access by themselves.",
        "Tokens should be random and URL-safe.",
    ])


class CreateVerificationChallengeRequest(BaseModel):
    purpose: str = "Phase 14 future request contract for creating a verification challenge."
    current_behavior: str = "No route creates verification challenges. This is a contract placeholder."
    target_id: str = Field(default="<uuid>", description="Target UUID to verify.")
    verification_method: str = Field(default="dns_txt", description="One of: dns_txt, html_meta_tag, well_known_file, manual_authorization, chatbot_api_challenge.")


class VerificationChallengeResponse(BaseModel):
    purpose: str = "Phase 14 future response contract for a created verification challenge."
    current_behavior: str = "No route returns live challenges. This is a contract placeholder."
    challenge_id: str = Field(default="<uuid>", description="Verification challenge record UUID.")
    target_id: str = Field(default="<uuid>", description="Target UUID.")
    verification_method: str = Field(default="dns_txt", description="Selected verification method.")
    challenge_value: str = Field(default="sherlock_<token>", description="Challenge token to place at the verification location.")
    instructions: str = Field(default="Follow the method-specific instructions to prove ownership.", description="Human-readable placement instructions.")
    expires_at: Optional[str] = Field(default=None, description="ISO 8601 expiry timestamp for the challenge.")
    status: str = Field(default="pending", description="Current verification status.")


class VerificationStatusResponse(BaseModel):
    purpose: str = "Phase 14 future response contract for verification status."
    current_behavior: str = "No route returns live verification status. This is a contract placeholder."
    target_id: str = Field(default="<uuid>", description="Target UUID.")
    verification_method: str = Field(default="dns_txt", description="Verification method used.")
    status: str = Field(default="unverified", description="Current status: unverified, pending, verified, failed, expired, manual_review_required.")
    verified_at: Optional[str] = Field(default=None, description="ISO 8601 timestamp when verification succeeded.")
    expires_at: Optional[str] = Field(default=None, description="ISO 8601 timestamp when verification expires.")


class VerificationContract(BaseModel):
    purpose: str = "Phase 14 verification API contract summary."
    current_behavior: str = "No route persists verification records, checks DNS/HTTP/chatbot targets, or unlocks scanning. All contracts are placeholder documentation."
    methods: VerificationMethodRegistry = Field(default_factory=VerificationMethodRegistry)
    statuses: VerificationStatusRegistry = Field(default_factory=VerificationStatusRegistry)
    challenge_token_design: ChallengeTokenDesign = Field(default_factory=ChallengeTokenDesign)
    create_challenge_request: CreateVerificationChallengeRequest = Field(default_factory=CreateVerificationChallengeRequest)
    challenge_response: VerificationChallengeResponse = Field(default_factory=VerificationChallengeResponse)
    status_response: VerificationStatusResponse = Field(default_factory=VerificationStatusResponse)
    security_boundaries: List[str] = Field(default_factory=lambda: [
        "No scan without verified target.",
        "No third-party target testing.",
        "No automatic crawling without SSRF controls.",
        "No fetching private/internal IPs, localhost, or metadata endpoints.",
        "No destructive actions during verification.",
        "No secrets in challenge values.",
        "Challenges should be random, short-lived, and non-sensitive.",
        "Verification attempts should be rate-limited in future phases.",
        "Verification logs may contain sensitive target metadata.",
        "Manual review needed for ambiguous targets.",
    ])
