#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
THEISM Advanced Intelligence Engine (TAI Engine)
===============================================

TAI Engine v1.0
Series foundation: TAI-1 through TAI-5
Next capability domain: Peace, Dialogue & Conflict Analysis

Purpose
-------
A training-oriented intelligence-analysis engine for:
- conflict analysis
- peace/dialogue process design
- mediation readiness
- stakeholder and power mapping
- inclusive process checks
- interest-based negotiation
- evidence / claim calibration
- competing-explanation analysis
- action planning

Design philosophy
-----------------
TAI is NOT a political persuasion engine and does not determine which
political actor is "right". It converts claims and observations into
structured analytical objects, makes assumptions visible, and forces
students to distinguish evidence from inference.

This engine is educational. It is not a substitute for professional
mediation, legal advice, humanitarian protection protocols, or security
risk assessment.

UN-aligned reference framework used in the curriculum:
- United Nations Guidance for Effective Mediation (2012)
- UN Declaration and Programme of Action on a Culture of Peace (1999)
- UN Women / Women, Peace and Security framework, including UNSCR 1325
- conflict-analysis and inclusive-mediation practice

Core TAI doctrine
-----------------
CLAIM -> EVIDENCE -> COMPETING EXPLANATIONS -> TEST -> ASSESSMENT -> UPDATE

The engine deliberately avoids:
- treating rhetoric as proof of implementation
- treating a number as a finding without a denominator/method
- equating neutrality with moral indifference
- assuming historical patterns automatically prove present behavior
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional
import json
import textwrap


ENGINE_NAME = "THEISM Advanced Intelligence Engine"
ENGINE_VERSION = "1.0.0"
SERIES = "TAI"
CLASSROOMS = "TAI-1 to TAI-5"


class EvidenceLevel(str, Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ClaimType(str, Enum):
    OBSERVATION = "observation"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"
    ASSESSMENT = "assessment"
    PREDICTION = "prediction"


@dataclass
class Evidence:
    description: str
    source_type: str = "unspecified"
    independence: float = 0.5       # 0..1
    reliability: float = 0.5        # 0..1
    directness: float = 0.5         # 0..1
    corroboration: float = 0.0      # 0..1
    date_relevance: float = 0.5     # 0..1

    def score(self) -> float:
        values = [
            self.independence,
            self.reliability,
            self.directness,
            self.corroboration,
            self.date_relevance,
        ]
        return round(mean(values), 3)


@dataclass
class Claim:
    text: str
    claim_type: ClaimType = ClaimType.HYPOTHESIS
    evidence: List[Evidence] = field(default_factory=list)
    confidence: float = 0.0

    def calculate_confidence(self) -> float:
        if not self.evidence:
            self.confidence = 0.0
            return self.confidence

        evidence_score = mean(item.score() for item in self.evidence)

        # Confidence is intentionally capped below certainty.
        # A training engine should preserve uncertainty.
        self.confidence = round(min(0.95, evidence_score), 3)
        return self.confidence


@dataclass
class Stakeholder:
    name: str
    position: str
    interests: List[str]
    needs: List[str]
    power: float = 0.5
    legitimacy: float = 0.5
    affectedness: float = 0.5
    inclusion_risk: float = 0.5

    def influence_score(self) -> float:
        return round(
            0.40 * self.power
            + 0.25 * self.legitimacy
            + 0.20 * self.affectedness
            + 0.15 * (1 - self.inclusion_risk),
            3,
        )


@dataclass
class ConflictIssue:
    name: str
    root_causes: List[str]
    intermediate_causes: List[str]
    triggers: List[str]
    visible_symptoms: List[str]
    connectors: List[str] = field(default_factory=list)
    dividers: List[str] = field(default_factory=list)


@dataclass
class MediationAssessment:
    preparedness: float
    consent: float
    impartiality: float
    inclusivity: float
    national_ownership: float
    legal_norms: float
    coherence: float
    coordination: float
    agreement_quality: float

    def overall_score(self) -> float:
        values = [
            self.preparedness,
            self.consent,
            self.impartiality,
            self.inclusivity,
            self.national_ownership,
            self.legal_norms,
            self.coherence,
            self.coordination,
            self.agreement_quality,
        ]
        return round(mean(values), 3)

    def weakest_dimensions(self, n: int = 3) -> List[str]:
        items = asdict(self)
        items.pop("overall_score", None)
        return [
            key for key, _ in sorted(items.items(), key=lambda pair: pair[1])[:n]
        ]


@dataclass
class NegotiationOption:
    name: str
    interests_served: List[str]
    objective_criteria: List[str]
    benefits: List[str]
    risks: List[str]
    feasibility: float = 0.5
    legitimacy: float = 0.5
    sustainability: float = 0.5

    def option_score(self) -> float:
        return round(
            0.40 * self.feasibility
            + 0.30 * self.legitimacy
            + 0.30 * self.sustainability,
            3,
        )


@dataclass
class CompetingExplanation:
    label: str
    explanation: str
    predictions: List[str]
    discriminators: List[str]
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)


class TAIEngine:
    """
    Main analytical engine.

    The engine is deliberately modular so future TAI classrooms can add
    specialized analyzers without changing the core data model.
    """

    def __init__(self, version: str = ENGINE_VERSION):
        self.version = version

    # ------------------------------------------------------------------
    # 1. CLAIM / EVIDENCE CALIBRATION
    # ------------------------------------------------------------------

    @staticmethod
    def calibrate_claim(claim: Claim) -> Dict[str, Any]:
        confidence = claim.calculate_confidence()

        if confidence < 0.25:
            level = EvidenceLevel.LOW
        elif confidence < 0.50:
            level = EvidenceLevel.MODERATE
        elif confidence < 0.75:
            level = EvidenceLevel.HIGH
        else:
            level = EvidenceLevel.VERY_HIGH

        return {
            "claim": claim.text,
            "claim_type": claim.claim_type.value,
            "confidence": confidence,
            "evidence_level": level.value,
            "evidence_count": len(claim.evidence),
            "analytical_warning": (
                "Do not convert this claim into fact without additional "
                "independent verification."
                if confidence < 0.75
                else "Confidence is relatively strong, but certainty is not assumed."
            ),
        }

    # ------------------------------------------------------------------
    # 2. CONFLICT TREE
    # ------------------------------------------------------------------

    @staticmethod
    def conflict_tree(issue: ConflictIssue) -> Dict[str, Any]:
        return {
            "root_causes": issue.root_causes,
            "intermediate_causes": issue.intermediate_causes,
            "triggers": issue.triggers,
            "visible_symptoms": issue.visible_symptoms,
            "connectors": issue.connectors,
            "dividers": issue.dividers,
            "analytical_rule": (
                "Do not confuse visible symptoms with root causes. "
                "Investigate causal links rather than assuming them."
            ),
        }

    # ------------------------------------------------------------------
    # 3. STAKEHOLDER / POWER ANALYSIS
    # ------------------------------------------------------------------

    @staticmethod
    def stakeholder_map(
        stakeholders: Iterable[Stakeholder],
    ) -> List[Dict[str, Any]]:
        ranked = sorted(
            stakeholders,
            key=lambda item: item.influence_score(),
            reverse=True,
        )

        result = []
        for s in ranked:
            result.append(
                {
                    "name": s.name,
                    "position": s.position,
                    "interests": s.interests,
                    "needs": s.needs,
                    "power": s.power,
                    "legitimacy": s.legitimacy,
                    "affectedness": s.affectedness,
                    "inclusion_risk": s.inclusion_risk,
                    "influence_score": s.influence_score(),
                }
            )
        return result

    # ------------------------------------------------------------------
    # 4. INCLUSION AUDIT
    # ------------------------------------------------------------------

    @staticmethod
    def inclusion_audit(stakeholders: Iterable[Stakeholder]) -> Dict[str, Any]:
        group_list = list(stakeholders)

        if not group_list:
            return {
                "score": 0.0,
                "status": "insufficient_data",
                "recommendations": ["Identify affected and excluded groups."],
            }

        avg_risk = mean(s.inclusion_risk for s in group_list)
        affected_without_voice = [
            s.name for s in group_list
            if s.affectedness >= 0.70 and s.inclusion_risk >= 0.60
        ]

        score = round(1 - avg_risk, 3)

        recommendations = []
        if affected_without_voice:
            recommendations.append(
                "Create safe consultation channels for highly affected groups."
            )
        if avg_risk > 0.50:
            recommendations.append(
                "Review representation, access, safety, language and power barriers."
            )
        recommendations.append(
            "Check meaningful participation, not merely presence on an attendance list."
        )

        return {
            "score": score,
            "status": "strong" if score >= 0.70 else "needs_attention",
            "high_risk_exclusion_groups": affected_without_voice,
            "recommendations": recommendations,
        }

    # ------------------------------------------------------------------
    # 5. MEDIATION READINESS
    # ------------------------------------------------------------------

    @staticmethod
    def mediation_readiness(
        assessment: MediationAssessment,
    ) -> Dict[str, Any]:
        score = assessment.overall_score()

        if score >= 0.80:
            status = "high_readiness"
        elif score >= 0.60:
            status = "moderate_readiness"
        elif score >= 0.40:
            status = "fragile_readiness"
        else:
            status = "low_readiness"

        return {
            "overall_score": score,
            "status": status,
            "weakest_dimensions": assessment.weakest_dimensions(),
            "principle_scores": asdict(assessment),
            "warning": (
                "A high score does not guarantee a successful peace process. "
                "It indicates stronger process conditions under the chosen rubric."
            ),
        }

    # ------------------------------------------------------------------
    # 6. INTEREST-BASED NEGOTIATION
    # ------------------------------------------------------------------

    @staticmethod
    def compare_options(
        options: Iterable[NegotiationOption],
    ) -> List[Dict[str, Any]]:
        ranked = sorted(
            options,
            key=lambda option: option.option_score(),
            reverse=True,
        )

        return [
            {
                "name": option.name,
                "interests_served": option.interests_served,
                "objective_criteria": option.objective_criteria,
                "benefits": option.benefits,
                "risks": option.risks,
                "feasibility": option.feasibility,
                "legitimacy": option.legitimacy,
                "sustainability": option.sustainability,
                "score": option.option_score(),
            }
            for option in ranked
        ]

    # ------------------------------------------------------------------
    # 7. COMPETING EXPLANATIONS
    # ------------------------------------------------------------------

    @staticmethod
    def compare_explanations(
        explanations: Iterable[CompetingExplanation],
        observations: Iterable[str],
    ) -> Dict[str, Any]:
        observations = list(observations)
        rows = []

        for explanation in explanations:
            matching = []
            conflicting = []

            observation_text = " ".join(observations).lower()

            for prediction in explanation.predictions:
                key_terms = [
                    word.lower().strip(".,!?")
                    for word in prediction.split()
                    if len(word) > 4
                ]
                if key_terms and sum(
                    term in observation_text for term in key_terms
                ) >= max(1, len(key_terms) // 3):
                    matching.append(prediction)

            for discriminator in explanation.discriminators:
                if discriminator.lower() in observation_text:
                    conflicting.append(discriminator)

            rows.append(
                {
                    "label": explanation.label,
                    "explanation": explanation.explanation,
                    "matched_predictions": matching,
                    "matched_discriminators": conflicting,
                    "supporting_evidence": explanation.supporting_evidence,
                    "contradicting_evidence": explanation.contradicting_evidence,
                }
            )

        return {
            "explanations": rows,
            "method_note": (
                "Keyword matching is only a training aid. Human analysts must "
                "validate semantic relevance and source quality."
            ),
        }

    # ------------------------------------------------------------------
    # 8. TRUTH-TELLER / INFORMATION-ENVIRONMENT TEST
    # ------------------------------------------------------------------

    @staticmethod
    def information_environment_test(
        bad_news_allowed: float,
        messenger_safety: float,
        contradiction_tolerance: float,
        negative_policy_response: float,
        independent_verification: float,
    ) -> Dict[str, Any]:
        values = [
            bad_news_allowed,
            messenger_safety,
            contradiction_tolerance,
            negative_policy_response,
            independent_verification,
        ]

        score = round(mean(values), 3)

        if score >= 0.75:
            interpretation = "relatively open_information_environment"
        elif score >= 0.50:
            interpretation = "mixed_or_fragile_information_environment"
        else:
            interpretation = "high_filtering_risk"

        return {
            "score": score,
            "interpretation": interpretation,
            "dimensions": {
                "bad_news_allowed": bad_news_allowed,
                "messenger_safety": messenger_safety,
                "contradiction_tolerance": contradiction_tolerance,
                "negative_policy_response": negative_policy_response,
                "independent_verification": independent_verification,
            },
            "core_test": (
                "Do not assess a truth-seeking instruction only by its wording. "
                "Measure what happens when inconvenient information appears."
            ),
        }

    # ------------------------------------------------------------------
    # 9. PEACE PROCESS ACTION PLAN
    # ------------------------------------------------------------------

    @staticmethod
    def action_plan(
        goal: str,
        actions: List[str],
        responsible_actors: List[str],
        timeline: List[str],
        indicators: List[str],
    ) -> Dict[str, Any]:
        lengths = {
            "actions": len(actions),
            "responsible_actors": len(responsible_actors),
            "timeline": len(timeline),
            "indicators": len(indicators),
        }

        return {
            "goal": goal,
            "actions": actions,
            "responsible_actors": responsible_actors,
            "timeline": timeline,
            "indicators": indicators,
            "completeness_check": lengths,
            "recommendation": (
                "Every action should have an accountable actor, a time horizon, "
                "and at least one observable indicator."
            ),
        }

    # ------------------------------------------------------------------
    # 10. STUDENT REPORT GENERATOR
    # ------------------------------------------------------------------

    def generate_report(
        self,
        title: str,
        claim_results: Optional[List[Dict[str, Any]]] = None,
        conflict_result: Optional[Dict[str, Any]] = None,
        stakeholder_result: Optional[List[Dict[str, Any]]] = None,
        inclusion_result: Optional[Dict[str, Any]] = None,
        mediation_result: Optional[Dict[str, Any]] = None,
        negotiation_result: Optional[List[Dict[str, Any]]] = None,
        information_result: Optional[Dict[str, Any]] = None,
    ) -> str:
        lines = [
            f"# {title}",
            "",
            f"**{ENGINE_NAME} v{self.version}**",
            "",
            "## Executive Assessment",
            "",
            "This report separates observations, evidence, hypotheses and "
            "assessment. It does not treat rhetoric as proof of implementation.",
            "",
        ]

        if claim_results:
            lines += ["## Claim Calibration", ""]
            for item in claim_results:
                lines += [
                    f"- **Claim:** {item['claim']}",
                    f"- **Type:** {item['claim_type']}",
                    f"- **Confidence:** {item['confidence']}",
                    f"- **Evidence level:** {item['evidence_level']}",
                    f"- **Warning:** {item['analytical_warning']}",
                    "",
                ]

        if conflict_result:
            lines += [
                "## Conflict Analysis",
                "",
                f"- Root causes: {', '.join(conflict_result['root_causes'])}",
                f"- Intermediate causes: {', '.join(conflict_result['intermediate_causes'])}",
                f"- Triggers: {', '.join(conflict_result['triggers'])}",
                f"- Visible symptoms: {', '.join(conflict_result['visible_symptoms'])}",
                "",
            ]

        if stakeholder_result:
            lines += ["## Stakeholder Analysis", ""]
            for item in stakeholder_result:
                lines.append(
                    f"- **{item['name']}** — influence score: "
                    f"{item['influence_score']}"
                )
            lines.append("")

        if inclusion_result:
            lines += [
                "## Inclusion Audit",
                "",
                f"- Score: {inclusion_result['score']}",
                f"- Status: {inclusion_result['status']}",
                "",
            ]
            for recommendation in inclusion_result["recommendations"]:
                lines.append(f"- {recommendation}")
            lines.append("")

        if mediation_result:
            lines += [
                "## Mediation Readiness",
                "",
                f"- Overall score: {mediation_result['overall_score']}",
                f"- Status: {mediation_result['status']}",
                f"- Weakest dimensions: "
                f"{', '.join(mediation_result['weakest_dimensions'])}",
                "",
            ]

        if negotiation_result:
            lines += ["## Negotiation Options", ""]
            for option in negotiation_result:
                lines.append(
                    f"- **{option['name']}** — score {option['score']}"
                )
            lines.append("")

        if information_result:
            lines += [
                "## Information Environment",
                "",
                f"- Score: {information_result['score']}",
                f"- Interpretation: {information_result['interpretation']}",
                "",
                f"> {information_result['core_test']}",
                "",
            ]

        lines += [
            "## Sentinel Closing",
            "",
            "> Claim → Evidence → Competing Explanations → Test → "
            "Assessment → Update",
            "",
            "**Confidence is conditional. New evidence should change the assessment.**",
        ]

        return "\n".join(lines)


def demo() -> None:
    """
    Demonstration using a hypothetical peace-dialogue scenario.
    No real-world actor is assigned a factual claim by the demo.
    """

    engine = TAIEngine()

    # TAI-5 lesson carried forward: distinguish claim from evidence.
    claim = Claim(
        text="A leadership instruction requesting truthful reporting may improve "
             "the information environment.",
        claim_type=ClaimType.HYPOTHESIS,
        evidence=[
            Evidence(
                description="Public instruction requesting more accurate reporting.",
                source_type="primary_statement",
                independence=0.5,
                reliability=0.7,
                directness=0.8,
                corroboration=0.2,
                date_relevance=0.9,
            ),
            Evidence(
                description="No independent evidence yet showing changed messenger safety.",
                source_type="analytical_gap",
                independence=0.7,
                reliability=0.5,
                directness=0.3,
                corroboration=0.0,
                date_relevance=0.8,
            ),
        ],
    )

    claim_result = engine.calibrate_claim(claim)

    issue = ConflictIssue(
        name="Hypothetical local conflict",
        root_causes=[
            "political exclusion",
            "institutional mistrust",
            "unequal access to decision-making",
        ],
        intermediate_causes=[
            "competing security perceptions",
            "economic pressure",
            "polarized information",
        ],
        triggers=[
            "a disputed administrative decision",
            "a violent incident",
        ],
        visible_symptoms=[
            "community displacement",
            "public protests",
            "breakdown of dialogue",
        ],
        connectors=[
            "shared local economic interests",
            "community leaders",
        ],
        dividers=[
            "identity polarization",
            "mutual fear",
        ],
    )

    conflict_result = engine.conflict_tree(issue)

    stakeholders = [
        Stakeholder(
            name="Community leaders",
            position="seek local stability",
            interests=["security", "livelihoods"],
            needs=["voice", "predictability"],
            power=0.55,
            legitimacy=0.80,
            affectedness=0.75,
            inclusion_risk=0.30,
        ),
        Stakeholder(
            name="Women-led civil society",
            position="seek inclusive peace",
            interests=["protection", "participation"],
            needs=["safety", "meaningful representation"],
            power=0.35,
            legitimacy=0.75,
            affectedness=0.85,
            inclusion_risk=0.70,
        ),
        Stakeholder(
            name="Youth representatives",
            position="seek future opportunities",
            interests=["education", "employment"],
            needs=["voice", "security"],
            power=0.30,
            legitimacy=0.65,
            affectedness=0.80,
            inclusion_risk=0.65,
        ),
    ]

    stakeholder_result = engine.stakeholder_map(stakeholders)
    inclusion_result = engine.inclusion_audit(stakeholders)

    mediation = MediationAssessment(
        preparedness=0.65,
        consent=0.55,
        impartiality=0.60,
        inclusivity=0.45,
        national_ownership=0.65,
        legal_norms=0.70,
        coherence=0.50,
        coordination=0.55,
        agreement_quality=0.40,
    )

    mediation_result = engine.mediation_readiness(mediation)

    options = [
        NegotiationOption(
            name="Inclusive local dialogue",
            interests_served=["security", "voice", "local legitimacy"],
            objective_criteria=["participation", "safety", "implementation"],
            benefits=["broader ownership", "early problem detection"],
            risks=["slow process", "spoiler behavior"],
            feasibility=0.65,
            legitimacy=0.85,
            sustainability=0.75,
        ),
        NegotiationOption(
            name="Closed elite agreement",
            interests_served=["rapid decision-making"],
            objective_criteria=["speed", "formal authority"],
            benefits=["fast initial agreement"],
            risks=["low ownership", "exclusion"],
            feasibility=0.80,
            legitimacy=0.45,
            sustainability=0.40,
        ),
    ]

    negotiation_result = engine.compare_options(options)

    information_result = engine.information_environment_test(
        bad_news_allowed=0.40,
        messenger_safety=0.35,
        contradiction_tolerance=0.45,
        negative_policy_response=0.40,
        independent_verification=0.70,
    )

    report = engine.generate_report(
        title="TAI Peace & Dialogue Demonstration Assessment",
        claim_results=[claim_result],
        conflict_result=conflict_result,
        stakeholder_result=stakeholder_result,
        inclusion_result=inclusion_result,
        mediation_result=mediation_result,
        negotiation_result=negotiation_result,
        information_result=information_result,
    )

    print(report)


def export_demo_json(path: str = "tai_engine_demo.json") -> None:
    """
    Export a compact machine-readable demo package.
    """
    engine = TAIEngine()

    package = {
        "engine": ENGINE_NAME,
        "version": engine.version,
        "series": SERIES,
        "classrooms": CLASSROOMS,
        "doctrine": [
            "Claim",
            "Evidence",
            "Competing Explanations",
            "Test",
            "Assessment",
            "Update",
        ],
        "supported_modules": [
            "claim_evidence_calibration",
            "conflict_tree",
            "stakeholder_power_analysis",
            "inclusion_audit",
            "mediation_readiness",
            "interest_based_negotiation",
            "competing_explanations",
            "information_environment_test",
            "action_planning",
            "student_report_generation",
        ],
    }

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(package, handle, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    demo()
