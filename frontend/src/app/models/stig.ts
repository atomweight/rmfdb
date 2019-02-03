export interface Stig {
  id: string;
  name: string;
  description: string;
  version: number;
  release: number;
  release_date: Date;
  rules: Rule[];
}

export interface StigsResponse {
  stigs: Stig[];
  total: number;
}

export interface Rule {
  id: string;
  group_id: string;
  group_title: string;
  full_rule_id: string;
  rule_id: string;
  rule_revision: string;
  rule_severity: string;
  rule_title: string;
  rule_metadata: RuleMetadata;
  check_content: string;
  fix_text: string;
  cves: string[];
  ccis: string[];
  stigs: Stig[];
}

export interface RuleMetadata {
  Documentable: boolean;
  VulnDiscussion: string;
  Mitigations: string;
  MitigationControl: string;
  version: string;
  mac_profiles: string[];
}
