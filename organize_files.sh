#!/bin/bash
# File organization script for opic

# Core language runtime
mv bootstrap.ops core/
mv opic_parse.ops core/
mv opic_load.ops core/
mv opic_execute.ops core/
mv core.ops core/
mv parser.ops core/
mv execute.ops core/
mv pure_execute.ops core/
mv self_execute.ops core/
mv python_boot.ops core/

# System capabilities
mv certificate.ops systems/
mv witness.ops systems/
mv signed.ops systems/
mv proof.ops systems/
mv vfs.ops systems/
mv vmap.ops systems/
mv voice_ledger.ops systems/
mv fee.ops systems/
mv generational_resonance.ops systems/
mv field_coherence.ops systems/
mv generate_field.ops systems/
mv resonance_currency.ops systems/
mv memory_bank.ops systems/
mv land_stewardship.ops systems/
mv recursive_contract_theory.ops systems/
mv learning_pools.ops systems/
mv governance.ops systems/
mv consensus.ops systems/
mv registry.ops systems/
mv treaty.ops systems/
mv opic_peer.ops systems/
mv witness_summons.ops systems/
mv vfs_audit.ops systems/
mv vfs_custody.ops systems/
mv vfs_ethics.ops systems/
mv vfs_nlp.ops systems/
mv vfs_quorum.ops systems/
mv vfs_demo.ops systems/
mv vfs_constitutional_demo.ops systems/
mv vmap_demo.ops systems/
mv planning_vfs.ops systems/
mv opic_plan_vfs.ops systems/
mv planning.ops systems/
mv opic_plan.ops systems/
mv blake.ops systems/
mv signature.ops systems/
mv ledger_sync.ops systems/
mv transition_funding.ops systems/
mv viral_resonance.ops systems/

# Wiki/documentation layer
mv tiddlywiki.ops wiki/
mv tiddlywiki_build.ops wiki/
mv tiddlywiki_network.ops wiki/
# tiddlers/ stays where it is, but we'll note it's part of wiki/

# Examples
mv example_signed.ops examples/
mv vfs_demo.ops examples/ 2>/dev/null || true
mv vfs_constitutional_demo.ops examples/ 2>/dev/null || true
mv vmap_demo.ops examples/ 2>/dev/null || true

# Tests
mv test.ops tests/
mv tests.ops tests/
mv runtime_test.ops tests/
mv test_interactive.ops tests/
mv test_ml.ops tests/
mv test_spec.ops tests/
mv test_self_compile.sh tests/

# Launch/application files stay in root
# (fee.ops, whitepaper.ops, company_seed.ops, etc. already moved to systems/)

echo "Files organized!"
