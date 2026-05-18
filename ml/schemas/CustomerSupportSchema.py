import pandera.pandas as pa

categories = ['ORDER', 'SHIPPING', 'CANCEL', 'INVOICE', 'PAYMENT', 'REFUND', 'FEEDBACK', 'CONTACT', 'ACCOUNT', 'DELIVERY', 'SUBSCRIPTION']
intents = ['cancel_order', 'change_order', 'change_shipping_address',
           'check_cancellation_fee', 'check_invoice', 'check_payment_methods',
           'check_refund_policy', 'complaint', 'contact_customer_service',
           'contact_human_agent', 'create_account', 'delete_account',
           'delivery_options', 'delivery_period', 'edit_account',
           'get_invoice', 'get_refund', 'newsletter_subscription',
           'payment_issue', 'place_order', 'recover_password',
           'registration_problems', 'review', 'set_up_shipping_address',
           'switch_account', 'track_order', 'track_refund']

class CustomerSupportSchema(pa.DataFrameModel):
    instruction: str = pa.Field()
    intent: str = pa.Field(isin=intents)
    category: str = pa.Field(isin=categories)
    response: str = pa.Field()
    response_len: int = pa.Field(gt=0)
    instruction_len: int = pa.Field(gt=0)
    #flags: str = pa.Field(str_matches=r"^[CWLMQIZPSENVBK]+$")
    flag_C: bool = pa.Field()
    flag_W: bool = pa.Field()
    flag_L: bool = pa.Field()
    flag_M: bool = pa.Field()
    flag_Q: bool = pa.Field()
    flag_I: bool = pa.Field()
    flag_Z: bool = pa.Field()
    flag_P: bool = pa.Field()
    flag_S: bool = pa.Field()
    flag_E: bool = pa.Field()
    flag_N: bool = pa.Field()
    flag_V: bool = pa.Field()
    flag_B: bool = pa.Field()
    flag_K: bool = pa.Field()
    has_order_number: bool = pa.Field()
    has_invoice_number: bool = pa.Field()
    has_person_name: bool = pa.Field()
    has_account_type: bool = pa.Field()
    has_account_category: bool = pa.Field()
    has_delivery_city: bool = pa.Field()
    has_delivery_country: bool = pa.Field()
    has_currency_symbol: bool = pa.Field()
    has_refund_amount: bool = pa.Field()