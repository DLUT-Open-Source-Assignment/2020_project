from mongoengine import *
import db_config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app_config import SECRET_KEY, EXPIRATOIN

connect(db_config.dbname, host=db_config.host, port=db_config.port, username=db_config.username, password=db_config.password, authentication_source=db_config.authentication_source)

# 歌曲实体
class Music_info(Document):
    title = StringField(required=True)
    artist = StringField()
    album = StringField()
    ext = StringField()
    collect = ListField(StringField())
    collect_size = LongField()
    contributor = StringField()

# 更新歌曲信息
def update_music_info(pk, param):
    music = Music_info.objects.get(pk=pk)
    music.title = param['title']
    music.artist = param['artist']
    music.album = param['album']
    music.save()

# 生成token
def generate_token(user):
    s = Serializer(SECRET_KEY, expires_in=EXPIRATOIN)
    token = s.dumps({'pk': str(user.pk)}).decode('ascii')
    return token

# 用户实体
class User_info(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    likes = ListField(ReferenceField(Music_info))
    my_music = ListField(ReferenceField(Music_info))

# 判断用户是否存在
def check_user(username, password):
    user = object()
    try:
        user = User_info.objects.get(username=username)
    except BaseException:
        return None
    else:
        token = generate_token(user)
        return token

# 创建用户
def new_user(username, password):        
    user = User_info(username=username, password=password)
    try:
        user.save(force_insert=True)
    except BaseException:
        return None
    else:
        return user

# 验证token
def vertify_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except BaseException:
        return None 
    return data['pk']

# 序列化歌曲列表
def serialization_music_list(musics):
    res = []
    for it in musics:
        tmp = {
            'pk' : str(it.pk),
            'title' : it['title'],
            'artist' : it['artist'],
            'album': it['album'],
            'collect_size': it['collect_size'],
            'contributor': it['contributor']
        }
        res.append(tmp)
    return res

# 根据主键获各歌曲
def get_music(pk):
    music = object()
    try:
        music = Music_info.objects.get(pk=pk)
    except BaseException:
        return None
    else:
        return music

# 根据主键获取收藏歌单
def like_list(pk):
    user = User_info.objects.get(pk=pk)
    return serialization_music_list(user.likes)

# 根据主键获取用户分析的歌曲
def my_music_list(pk):
    user = User_info.objects.get(pk=pk)
    for it in user.my_music:
        print(it.title)
    return serialization_music_list(user.my_music)

# 根据token判断用户名称
def username(token):
    user = User_info.objects.get(pk=str(vertify_token(token)))
    return user.username

# 新建歌曲
def new_music_info(contributor, ext):
    music = Music_info(title='temp', ext=ext, contributor=contributor, collect_size=0)
    user = User_info.objects.get(username=contributor)
    music.save()
    user.update(push__my_music=music)
    return music.pk

# 收藏歌曲
def like_music(token, music_id):
    music = Music_info.objects.get(pk=music_id)
    if music == None:
        return False
    user_id = vertify_token(token)
    music.update(add_to_set__collect=user_id)
    music.update(inc__collect_size=1)
    user = User_info.objects.get(pk=user_id)
    user.update(add_to_set__likes=music)
    return True

# 获取歌曲收藏排行l-r的歌曲
def get_music_inorder(l, r):
    musics = Music_info.objects.order_by("-collect_size")[l:r]
    return {'res': serialization_music_list(musics), 'len' : Music_info.objects.count()}

    