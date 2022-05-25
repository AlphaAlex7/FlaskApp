def do_disable_forms(form):
    """for post forms"""
    for field in form:
        form[field.name].render_kw = {'disabled': 'disabled'}
        form[field.name].description = "Запись уже опубликована"


def form_to_model(form, model):
    for field in form:
        if hasattr(model, field.name):
            model.__setattr__(field.name, form[field.name].data)
    return model


def model_to_form(form, model):
    for field in form:
        if hasattr(model, field.name):
            form[field.name].data = model.__getattribute__(field.name)
    return model
