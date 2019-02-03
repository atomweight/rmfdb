export interface Control {
  id: string;
  control_id: string;
  family: string;
  family_acronym: string;
  guidance: string;
  name: string;
  text: string;
  confidentiality_threshold: string;
  integrity_threshold: string;
  availability_threshold: string;
  ccis: Cci[];
}

export interface ControlsResponse {
  controls: Control[];
  total: number;
}

export interface Cci {
  id: string;
  cci_id: string;
  ap_acronym: string;
  text: string;
  auditor_guidance: string;
  org_guidance: string;
  control: Control;
}
