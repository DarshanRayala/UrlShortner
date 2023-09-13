EMAIL_USE_TLS='True'
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='djangoa16@gmail.com'
EMAIL_HOST_PASSWORD='DjangoMail_01'
EMAIL_PORT='587'
SECRET_KEY='django-insecure-bh1xguvcqf$mpm2+wuoa=qn(90%d4@(k=*=s4tmn*nnwviz9m&'
# import environ
# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )
# # reading .env file
# environ.Env.read_env()


# EMAIL_HOST = env('EMAIL_HOST', default='localhost')
# EMAIL_PORT = env('EMAIL_PORT', default=25, cast=int)
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
# EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=False, cast=bool)