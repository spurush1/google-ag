export type AGUIComponentType = 
  | 'text'
  | 'markdown'
  | 'risk-card'
  | 'bom-tree'
  | 'supplier-table'
  | 'json';

export interface AGUIComponent {
  type: AGUIComponentType;
  data: any;
  title?: string;
}

export interface AGUIMessage {
  message: string;
  components: AGUIComponent[];
}

