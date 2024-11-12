import datetime
import discord
import asyncio

FAST_REFRESH_MODE = False

# Add more users here
ProfileToUidMapping = {
        "Gabe" : 650140370193219594, 
        "Derrick" : 650140370193219594,
        "Ahmed" : 912550670597488661,
    }

TOKEN = ""
ValorSucessChannel = 1147380412629397585
CyberSuccessChannel = 1156836773306048553
AlpineSucessChannel = 1200723508368506983
MakeSuccessChannel = 1269784402712461382
SwiftSuccessChannel = 1288267605647429692
RefractSucessChannel = 1293669222026842164
StellarSuccessChannel = 1288854903174729748
AcoSuccessChannel = 1160270200998989844
processedMessages = []

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def check_new_messages(channelDict):
    while True:
        for channel, value in channelDict.items():
            try:
                async for message in channel.history(limit=75 if FAST_REFRESH_MODE else 20):

                    current_time = datetime.datetime.now(datetime.timezone.utc)
                    time_difference = current_time - message.created_at

                    if time_difference.total_seconds() <= 45:
                        if message.id not in processedMessages:
                            getUid(message, value)
                            processedMessages.append(message.id)

            except discord.errors.DiscordServerError:
                print("Discord server error occurred. Retrying in a few seconds...")
                await asyncio.sleep(15)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            await asyncio.sleep(0.5 if FAST_REFRESH_MODE else 1.5)











# Mark: Ignore --------------------- ---------------------- ----------------------

def getUid(message, value):
        
    def check_card_declined():
        if "card decline" in message.content.lower():
            return True
        if message.embeds:
            for embed in message.embeds:
                if embed.title and "card decline" in embed.title.lower():
                    return True
                if embed.description and "card decline" in embed.description.lower():
                    return True
                for field in embed.fields:
                    if field.name and "card decline" in field.name.lower():
                        return True
                if embed.footer and embed.footer.text and "card decline" in embed.footer.text.lower():
                    return True
        return False

    # Return early if "card declined" is found
    if check_card_declined():
        return
        
    names = set(ProfileToUidMapping.keys())

    message_content = message.content.lower()
    found_name = next((name for name in names if name.lower() in message_content), None)

    if not found_name and message.embeds:
        for embed in message.embeds:
            # Check embed title
            if embed.title and (found_name := next((name for name in names if name.lower() in embed.title.lower()), None)):
                break
            
            # Check embed description
            if embed.description and (found_name := next((name for name in names if name.lower() in embed.description.lower()), None)):
                break
            
            # Check all fields within the embed
            for field in embed.fields:
                if field.name and (found_name := next((name for name in names if name.lower() in field.name.lower()), None)):
                    break
                if field.value and (found_name := next((name for name in names if name.lower() in field.value.lower()), None)):
                    break
            if found_name:
                break

            # Check footer text
            if embed.footer and embed.footer.text and (found_name := next((name for name in names if name.lower() in embed.footer.text.lower()), None)):
                break

            # Check image URL (although it's unlikely names are here)
            if embed.image and embed.image.url and (found_name := next((name for name in names if name.lower() in embed.image.url.lower()), None)):
                break

    uid = ProfileToUidMapping[found_name] if found_name else None

    if value == 1:
        handleValor(message, uid)
    elif value == 2:
        handleCyber(message, uid)
    elif value == 3:
        handleAlpine(message, uid)
    elif value == 4:
        handleMake(message, uid)
    elif value == 5:
        handleSwift(message, uid)
    elif value == 6:
        handleRefract(message, uid)
    elif value == 7:
        handleStellar(message, uid)

def handleValor(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    if field.name.lower() == "product":
                        product = field.value
                    elif field.name.lower() == "site":
                        site = field.value
                    elif field.name.lower() == "size":
                        size = field.value
                    elif field.name.lower() == "profile":
                        profile = field.value
                    elif field.name.lower() == "order":
                        order = field.value
                    elif field.name.lower() == "orderlink":
                        orderLink = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleCyber(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.description:
                product = embed.description.split('\n')[0]

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "store":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order":
                        order = field.value

                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").replace("|", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleAlpine(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "site:":
                        site = field.value
                    elif field_name == "size:":
                        size = field.value
                    elif field_name == "profile:":
                        profile = field.value
                    elif field_name == "order:":
                        order = field.value

                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()
                    elif field_name == "product:":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleMake(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:

            if embed.description:
                site = embed.description.strip()

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")

                    elif field_name == "size":
                        if not size:
                            size = field.value
                    elif field_name == "profile name":
                        profile = field.value
                    elif field_name == "order":
                        order = field.value
                        # Extract order ID and order link from the order string if applicable
                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.title:
                order = embed.title  # Set order as the title of the embed
            if embed.url:
                orderLink = embed.url  # Set orderLink as the embed URL

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleSwift(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.strip().lower()
                    if field_name == "**site**":
                        site = field.value
                    elif field_name == "**item**":
                        product = field.value
                    elif field_name == "**profile**":
                        profile = field.value
                    elif field_name == "**order #**":
                        order = field.value.replace("||", "").strip()
                    elif field_name == "**size**":
                        size = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleRefract(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")
                    elif field_name == "price":
                        pass
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order number":
                        order = field.value
                        # Extract order ID and order link from the order string if applicable
                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            order.replace('|', '').strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleStellar(message, uid):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        product = field.value
                    elif field_name == "site":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

async def sendMessage(uid, product, thumbnail_url, site, size, profile, orderLink, order):
    profile = profile.replace("|", "").strip()

    if uid is not None:
        user = await client.fetch_user(uid)

        if user is not None:
            description_parts = [
                f"**Product**: {product}",
                f"**Site**: {site}",
                f"**Size**: {size}",
                f"**Profile**: {profile}"
            ]

            if order or orderLink:
                description_parts.append(
                    f"**Order**: [{order}]({orderLink})"
                )

            description = "\n".join(description_parts)

            embed = discord.Embed(
                title="Wealth ACO Success",
                description=description,
                color=0x791313
            )

            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)

            await user.send(embed=embed)
        else:
            print("User not found.")

    await sendPublicMessage(product, thumbnail_url, site, size, profile, uid)

async def sendPublicMessage(product, thumbnail_url, site, size, profile, uid):
    valor = client.get_channel(AcoSuccessChannel)

    description_parts = [
        f"**Product**: {product}",
        f"**Site**: {site}",
        f"**Size**: {size}",
        f"**Profile**: || {profile} ||"
    ]

    description = "\n".join(description_parts)

    embed = discord.Embed(
        title="Wealth ACO Success",
        description=description,
        color=0x791313
    )

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    if uid is not None:
        tag = f"<@{uid}>"

        await valor.send(f"{tag}\n", embed=embed)
    else:
        await valor.send(embed=embed)

@client.event
async def on_ready():
    valor = client.get_channel(ValorSucessChannel)
    cyber = client.get_channel(CyberSuccessChannel)
    alpine = client.get_channel(AlpineSucessChannel)
    make = client.get_channel(MakeSuccessChannel)
    swift = client.get_channel(SwiftSuccessChannel)
    refract = client.get_channel(RefractSucessChannel)
    stellar = client.get_channel(StellarSuccessChannel)

    channelDict = {
        valor : 1,
        cyber : 2,
        alpine : 3,
        make : 4,
        swift : 5,
        refract : 6,
        stellar : 7,
    }

    await check_new_messages(channelDict)

client.run(TOKEN)
