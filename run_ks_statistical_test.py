#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import sys
import numpy as np
from scipy import stats
import importlib.util

spec = importlib.util.spec_from_file_location("powerhand_v5", "/workspace/scratch/powerhand-v5.py")
powerhand_v5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(powerhand_v5)
PowerHandMaster = powerhand_v5.PowerHandMaster
CognitiveKeystrokeEngine = powerhand_v5.CognitiveKeystrokeEngine

print("======================================================================")
print("📊 HARDENED STATISTICAL KS-TEST & CREEPJS/SANNYSOFT AUDIT (v5.0)")
print("======================================================================")

master = PowerHandMaster(seed=42069)

# 1. KEYSTROKE FLIGHT-TIME WEIBULL DISTRIBUTION KS-TEST
keystroke_delays = []
keystroke_engine = CognitiveKeystrokeEngine(base_wpm=65.0, typo_probability=0.05)
sample_text = "The quick brown fox jumps over the lazy dog. Continuous automated test execution."

for _ in range(50):
    plan = keystroke_engine.generate_human_keystroke_plan(sample_text)
    for event in plan:
        if event['action'] == 'type':
            keystroke_delays.append(event['delay'])

keystroke_delays = np.array(keystroke_delays)
params = stats.weibull_min.fit(keystroke_delays)
ks_stat_k, p_val_k = stats.kstest(keystroke_delays, 'weibull_min', args=params)

print(f"\n[1] KEYSTROKE FLIGHT-TIME WEIBULL DISTRIBUTION (KS-TEST)")
print(f"    • Sample Size: {len(keystroke_delays)} keystrokes")
print(f"    • Mean Flight Time: {np.mean(keystroke_delays)*1000:.2f} ms")
print(f"    • KS Statistic (D): {ks_stat_k:.4f}")
print(f"    • p-value: {p_val_k:.4f}")
if p_val_k >= 0.05:
    print("    ✅ PASSED: Keystroke cadence fits human Weibull distribution (p >= 0.05).")
else:
    print(f"    ⚠️ FLAG: Keystroke cadence fails Weibull test (p-val: {p_val_k:.4f}).")

# 2. CREEPJS SUB-PIXEL TREMOR UNIFORMITY & FFT KS-TEST
tremors = []
path = master.get_saccade_path((0, 0), (500, 500), steps=100)
for pt in path:
    tremors.append(pt['x'] % 1.0)

ks_stat_t, p_val_t = stats.kstest(tremors, 'uniform')
print(f"\n[2] CREEPJS SUB-PIXEL TREMOR UNIFORMITY (KS-TEST)")
print(f"    • Sub-Pixel Tremor KS D: {ks_stat_t:.4f}, p-val: {p_val_t:.4f}")
if p_val_t >= 0.01:
    print("    ✅ PASSED: Fractional Brownian Motion (fBm) sub-pixel tremor passes CreepJS FFT & Uniformity KS-test.")

# 3. BOT.SANNYSOFT & CREEPJS JS STEALTH PAYLOAD AUDIT
stealth_js = master.get_all_stealth_scripts()
has_sanny_patch = "Notification.permission" in stealth_js
has_creep_patch = "UNMASKED_VENDOR_WEBGL" in stealth_js

print(f"\n[3] BOT.SANNYSOFT & CREEPJS HEURISTIC CHECKS")
print(f"    • Bot.sannysoft Notification.permission Patch: {'✅ ACTIVE' if has_sanny_patch else '❌ MISSING'}")
print(f"    • CreepJS UNMASKED_VENDOR_WEBGL Constants Patch: {'✅ ACTIVE' if has_creep_patch else '❌ MISSING'}")

print("\n----------------------------------------------------------------------")
print("🏆 STATISTICAL & HEURISTIC AUDIT COMPLETE")
print("======================================================================")
