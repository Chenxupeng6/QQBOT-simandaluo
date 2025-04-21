# -*- coding: utf-8 -*-
import asyncio
import os
import re
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from urllib.parse import quote
from botpy.message import C2CMessage
from botpy.ext.cog_yaml import read

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        bot_mention_pattern = re.compile(rf"<@!?{self.robot.id}>\s*")
        clean_content = bot_mention_pattern.sub("", message.content).strip()
        _log.info(f"清理后内容: {clean_content}")

        parts = clean_content.split(maxsplit=1)
        if not parts:
            return  # 空指令不处理

        command = parts[0].lower()
        file_name = ""

        # 指令匹配
        if command in ["/菜单", "菜单"]:
            file_name = "菜单.png"
        elif command in ["/个人装备表", "个人装备表"]:
            file_name = "个人武器.png"
        elif command in ["/飞船", "飞船"]:
            if len(parts) < 2 or not parts[1].strip():
                # 修正：使用API发送文本消息
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,  # 0表示文本类型
                    content="🚫 请输入飞船名称，例如：/飞船 北极星",
                    msg_id=message.id
                )
                return
            ship_name = parts[1].strip()
            file_name = f"{ship_name}.png"
        else:
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                content="❓ 未知指令，支持指令：\n/菜单\n/个人装备表\n/飞船 [名称]",
                msg_id=message.id
            )
            return

        # URL编码处理
        encoded_name = quote(file_name)
        file_url = f"https://www.simandaluo.cn/cstu/{encoded_name}"
        
        try:
            uploadMedia = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,
                url=file_url
            )
            
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=uploadMedia
            )
        except Exception as e:
            _log.error(f"发送文件失败：{str(e)}")
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                content="⚠️ 获取资源失败，请稍后再试",
                msg_id=message.id
            )
    async def on_c2c_message_create(self, message: C2CMessage):
        bot_mention_pattern = re.compile(rf"<@!?{self.robot.id}>\s*")
        clean_content = bot_mention_pattern.sub("", message.content).strip()
        _log.info(f"清理后内容: {clean_content}")

        parts = clean_content.split(maxsplit=1)
        if not parts:
            return  # 空指令不处理

        command = parts[0].lower()
        file_name = ""

        # 指令匹配
        if command in ["/菜单", "菜单"]:
            file_name = "菜单.png"
        elif command in ["/个人装备表", "个人装备表"]:
            file_name = "个人武器.png"
        elif command in ["/飞船", "飞船"]:
            if len(parts) < 2 or not parts[1].strip():
                # 修正：使用API发送文本消息
                await message._api.post_c2c_message(
                    openid=message.author.user_openid, 
                    msg_type=0,  # 0表示文本类型
                    content="🚫 请输入飞船名称，例如：/飞船 北极星",
                    msg_id=message.id
                )
                return
            ship_name = parts[1].strip()
            file_name = f"{ship_name}.png"
        else:
            await message._api.post_c2c_message(
                openid=message.author.user_openid, 
                msg_type=0,
                content="❓ 未知指令，支持指令：\n/菜单\n/个人装备表\n/飞船 [名称]",
                msg_id=message.id
            )
            return

        # URL编码处理
        encoded_name = quote(file_name)
        file_url = f"https://www.simandaluo.cn/cstu/{encoded_name}"
        
        try:
            uploadMedia = await message._api.post_c2c_file(
                openid=message.author.user_openid, 
                file_type=1,
                url=file_url
            )
            
            await message._api.post_c2c_message(
                openid=message.author.user_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=uploadMedia
            )
        except Exception as e:
            _log.error(f"发送文件失败：{str(e)}")
            await message._api.post_c2c_message(
                openid=message.author.user_openid, 
                msg_type=0,
                content="⚠️ 获取资源失败，请稍后再试",
                msg_id=message.id
            )
if __name__ == "__main__":
    app_id = "102756167"
    app_secret = "V1X3Z5b7dAhElIpMuS0Y6eCkJsR0Z8hH"

    intents = botpy.Intents(public_guild_messages=True,public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=app_id, secret=app_secret)