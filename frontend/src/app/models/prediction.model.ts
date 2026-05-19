export type SupportCategory =
  | 'ORDER'
  | 'SHIPPING'
  | 'CANCEL'
  | 'INVOICE'
  | 'PAYMENT'
  | 'REFUND'
  | 'FEEDBACK'
  | 'CONTACT'
  | 'ACCOUNT'
  | 'DELIVERY'
  | 'SUBSCRIPTION';

export interface PredictionRequest {
  instruction: string;
}

export interface PredictionResponse {
  prediction: SupportCategory;
  confidence: number | null;
  model_version: string;
  pipeline_version: string;
}
