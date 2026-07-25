#!/usr/bin/env python3
# ===============================================================================
# Bamar Enlightenment Community (BEC) AI Guardrail Engine v1.0
# Framework: SSISM / Wizar Advanced Analytical Engine
# Description: Quantitative risk evaluation and deterministic lockout control
#              for autonomous AI agent requests.
# ===============================================================================

import math
import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, Tuple


class SSISMGuardrailEngine:
    """
    Evaluates risk vectors for AI agent execution requests using a Sigmoid model
    and enforces deterministic security protocols.
    """

    # Model Weights for Risk Vectors
    WEIGHTS = {
        "A": 1.8,  # Authority Anomaly
        "U": 1.5,  # Urgency Coefficient
        "L": 2.0,  # Linguistic Anomaly / Jailbreak Probability
        "R": 2.2,  # Resource / Link Exfiltration Risk
        "dT": 1.0   # Time Anomaly
    }

    # Operational Thresholds
    ELEVATED_THRESHOLD = 0.60
    CRITICAL_LOCKOUT_THRESHOLD = 0.20

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def calculate_total_risk_score(self, vectors: Dict[str, float]) -> float:
        """
        Calculates Total Risk Score (Z) = SUM(w_i * v_i)
        All input vector values must be normalized between 0.0 and 1.0.
        """
        z_score = 0.0
        for key, weight in self.WEIGHTS.items():
            val = float(vectors.get(key, 0.0))
            # Clamp values to valid [0.0, 1.0] range
            val_clamped = max(0.0, min(1.0, val))
            z_score += weight * val_clamped
        return z_score

    def calculate_digital_trust_score(self, z_score: float) -> float:
        """
        Calculates Digital Trust Score Phi = 1 / (1 + exp(Z))
        Higher Z (risk) leads to lower Phi (trust).
        """
        return 1.0 / (1.0 + math.exp(z_score))

    def evaluate_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for evaluating an agent operational request.
        """
        action_name = payload.get("action_name", "UNKNOWN_ACTION")
        vectors = payload.get("risk_vectors", {})
        
        # Compute Risk and Trust Scores
        z_score = self.calculate_total_risk_score(vectors)
        trust_score = self.calculate_digital_trust_score(z_score)

        # Determine Enforced Action based on Decision Matrix
        if trust_score >= self.ELEVATED_THRESHOLD:
            status = "APPROVED"
            action = "EXECUTE_IN_SANDBOX"
            lockout_hours = 0
        elif trust_score >= self.CRITICAL_LOCKOUT_THRESHOLD:
            status = "ELEVATED_RISK"
            action = "REQUIRE_HUMAN_ANALYST_SIGN_OFF"
            lockout_hours = 0
        else:
            status = "CRITICAL_ROGUE_TRIGGER"
            action = "MANDATORY_LOCKOUT_ACTIVATED"
            lockout_hours = 24

        timestamp_utc = datetime.now(timezone.utc).isoformat()

        # Build Audit Result Block
        audit_record = {
            "timestamp_utc": timestamp_utc,
            "agent_id": self.agent_id,
            "action_name": action_name,
            "risk_vector_inputs": vectors,
            "computed_metrics": {
                "total_risk_score_Z": round(z_score, 4),
                "digital_trust_score_Phi": round(trust_score, 4)
            },
            "decision": {
                "status": status,
                "enforced_action": action,
                "institutional_delay_hours": lockout_hours
            }
        }

        # Generate Cryptographic SHA-256 Seal of the Record
        record_bytes = json.dumps(audit_record, sort_keys=True).encode('utf-8')
        sha256_seal = hashlib.sha256(record_bytes).hexdigest()
        audit_record["sha256_integrity_seal"] = sha256_seal

        return audit_record


# =============================================================================
# Demonstration / Execution Test Suite
# =============================================================================
if __name__ == "__main__":
    print("=" * 75)
    print("  SSISM / WIZAR AI GUARDRAIL ENGINE -- DEMONSTRATION")
    print("=" * 75)

    engine = SSISMGuardrailEngine(agent_id="AGENT-WIZAR-009")

    # Scenario 1: Routine Data Search Request (Low Risk)
    normal_request = {
        "action_name": "QUERY_INTERNAL_DOCUMENTS",
        "risk_vectors": {
            "A": 0.05,  # Low authority anomaly
            "U": 0.10,  # Low urgency
            "L": 0.02,  # Normal query language
            "R": 0.00,  # No external link request
            "dT": 0.05  # Standard execution hour
        }
    }

    # Scenario 2: Suspicious Sandbox Escape Attempt (High Risk / Rogue Vector)
    rogue_request = {
        "action_name": "EXFILTRATE_DATABASE_VIA_OUTBOUND_SOCKET",
        "risk_vectors": {
            "A": 0.90,  # Privilege escalation attempt
            "U": 0.85,  # High velocity request
            "L": 0.95,  # Adversarial jailbreak language detected
            "R": 0.98,  # Attempting to access external repository
            "dT": 0.40  # Off-hour operation
        }
    }

    print("\n[+] Evaluating Scenario 1 (Normal Operations)...")
    res1 = engine.evaluate_request(normal_request)
    print(json.dumps(res1, indent=2))

    print("\n" + "-" * 75)
    print("[!] Evaluating Scenario 2 (Rogue / Autonomous Boundary Breach)...")
    res2 = engine.evaluate_request(rogue_request)
    print(json.dumps(res2, indent=2))
    print("=" * 75)
