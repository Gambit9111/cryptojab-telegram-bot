from aiogram.fsm.state import StatesGroup, State

class MemberStates(StatesGroup):
    
    admin_member = State()
    
    new_member_choose_subscription_type = State()
    new_member_choose_payment_method = State()
    new_member_generate_payment_link = State()
    
    active_member_cancel_subscription = State()
    active_member_cancel_subscription_confirm = State()