import { Cci, Control } from './control';
import { Rule, Stig } from './stig';


export interface SearchResponse {
  stigs: Stig[];
  rules: Rule[];
  ccis: Cci[];
  controls: Control[];
}
