





import requests

cook='appbot_convert={%22referer%22:null%2C%22landing%22:%22https://appbot.co/%22}; _ga=GA1.2.30329182.1540298320; intercom-id-glvjson7=f3876d87-0fec-45f4-89f2-85f1209950c4; appbot_session_active=true; cookieconsent_status=allow; intercom-session-glvjson7=UlhJK3ZCTHF6dFlBLzNVV2IyZDhjaWNSWTc4cDRuN2dZZ0dRa2dyMjZBd21SUlpJT0xnVlJ6ZzkxQlFiZTdUby0tbjRtS0hjS3hUenNxT1o5RDZOanUzQT09--223ba2c3f3a550394ee3dd5ad077e76c32fc0be0; remember_user_token=BAhbCFsGaQJOkkkiIiQyYSQxMCQxN0FGZHNDZ050RmRwT2JSRElDalguBjoGRVRJIhcxNTQwNDM2NDA4Ljk2MjM3NDcGOwBG--578f0df79fd57a0bc670f3b164c91fb874fa529d; _gid=GA1.2.998133860.1540436421; _gat=1; _hp2_id.116503402=%7B%22userId%22%3A%227121901154332925%22%2C%22pageviewId%22%3A%228825843111957251%22%2C%22sessionId%22%3A%222353689844032949%22%2C%22identity%22%3A%221509662199%40qq.com%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _hp2_ses_props.116503402=%7B%22ts%22%3A1540436420819%2C%22d%22%3A%22app.appbot.co%22%2C%22h%22%3A%22%2Fapps%2F1393448-arena-of-valor%2Freviews%22%7D; _appbot_session=eURGbk02K0Zpbnh5a2dNVnpHc0drWGc3aGtDWTRQZEZldVI5M0NtYS9JTlQvTW5UZldPRmR3c1RMS2FtcVN0TzV5dXVWRjlmOGQxQ29NRTM0aUlqTlNLKzloUkdJUVk3M2lwaFlmc2VlWDdscWFZMDNFM0drVXozSU4vcnVERjlrRVFMME0yNWhOQnpWVUI5a1QxWUNTMXpXUWhqdmRNdCsxaUhpT29UMmZHa3dPMWZuTWxyckFUWExLTndqNTNTMVh5aThmN05qTjNmTHpUNFBjL1hDL2d1NHIydjNMQThDL1lmVmZyem9VTlJKMWJkZ3ZRNUlSS2RaRkgyc2NETll3QWoxZ3NDR1FwZmp3N2MrSXlabEhhblM0UVdlVklvaHFYYlIrN3d0dGhtRGZaaDBqQUtQa1RadUhUYzVDaHFIZ2JNUVJpN2RuMHZEQlZOVHlpNkhzRlJUT1Y1MDNDc0UxNmRiNGd5WWFnPS0tR296UWQramlRU1NXZGVEN2R5d3VDQT09--875d723f0968d9abea12c03687e14f9c665ffae2; filterOpen=true'
header={
    'Cookie':cook,
    'referer':'https://app.appbot.co/apps/1393448-arena-of-valor/reviews',
    's':'980fb71da83a2a5e09431e5023b2e5373f7dbc7f',
    # 's':'786e31f6befa521723b0afe90eca31f937d09190'
    # 's':'7f581ec28840d94a3e84b61431ef62617e568273'
    # 's':'df760c8aecd6c8a60ab5f5d1fd61dda9ad1b3ee0'
    # 's':'7cab2996fdc06853ea6c4e7db9511680d5a8408a'
    # 's':'b2576c0bd7fafb1fa3dad789846ce7f769055419'
}

url='https://app.appbot.co/apps/1393448-arena-of-valor/reviews#/?dlangs=zh&end=2018-10-25&start=2018-07-27'
url='https://app.appbot.co/data/apps/1393448/reviews?start=2018-07-27&end=2018-10-25&dlangs=zh&count=10&page=1'
url='https://app.appbot.co/data/apps/10242/reviews?start=2018-07-27&end=2018-10-25&dlangs=zh-Hant&count=10&page=1'
url='https://app.appbot.co/data/apps/10242/reviews?start=2018-07-27&end=2018-10-25&dlangs=zh&count=10&page=1'
# url='https://app.appbot.co/data/apps/1393448/reviews?start=2018-07-27&end=2018-10-25&dlangs=zh&count=10&page=2&____c=c7d8c9c8e91be712870923d832de2fdd43b5a4bf'
# url='https://app.appbot.co/data/apps/1393448/reviews?start=2018-07-27&end=2018-10-25&dlangs=zh&count=10&page=3'
req=requests.get(url,headers=header)
print(req.text)