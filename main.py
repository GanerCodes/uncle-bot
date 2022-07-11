import basc_py4chan, requests, discord, string, random, html, os, re

fixedHtmlParser = lambda body: re.sub(r'<.+?>', '', re.sub(r'<a [^>]+>(.+?)</a>', r'\1', html.unescape(body)).replace('<br>', '\n'))

if not os.path.isdir("images"): os.mkdir("images")

def genPost():
    board = basc_py4chan.Board('x')
    post = board.get_thread(random.choice(board.get_all_thread_ids())).all_posts[0]
    with open(filename := ("images/" + (''.join(random.choice(string.ascii_letters) for i in range(9))) + os.path.splitext(post.file.filename)[1]), "wb") as f:
        f.write(requests.get(post.file.file_url).content)
    return (post.subject + '\n' if post.subject else "")[:2000] + fixedHtmlParser(post.comment), filename

bot = discord.Client()
@bot.event
async def on_ready():
    print("READY")

@bot.event
async def on_message(msg):
    if int(random.random() * 256) == 0 or msg.content == 'idk whats uncle gotta say about that':
        print("Uncle.")
        post = genPost()
        if random.random() < 0.5:
            await msg.reply(post[0], files = [discord.File(post[1])])
        else:
            await msg.channel.send(post[0], files = [discord.File(post[1])])
        os.remove(post[1])

bot.run("TOKEN")
