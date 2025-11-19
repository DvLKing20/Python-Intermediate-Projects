import argparse
import aiohttp
import time
from pathlib import Path
import asyncio
from aiohttp import ClientConnectionError, ClientConnectorError
from rich.progress import Progress

class CLI_downloder:

    def __init__(self):
        self.sessions = []
        self.parser = argparse.ArgumentParser(description="DvLKing20 Downloader", prog="KingTool")
        self.add_arguments()
        self.parse = self.parser.parse_args()
        self.path = Path(self.parse.path)
        self.path.mkdir(parents=True, exist_ok=True)


    async def fetch_stop(self):
        while True:
          try:
            print(len(self.sessions))
            kill_task = await asyncio.to_thread(input, "Which task to kill?:")
            kill_task = int(kill_task)-1
            self.sessions[kill_task].cancel()
          except ValueError:
            print("Invalid input")
          except IndexError:
            print("Invalid index")


    async def fetch_data(self,session,url,progress):
        try:
            file_name = self.path / url.split('/')[-1]
            async with session.get(url) as resp:
              size = int(resp.headers.get("Content-Length",0))
              task = progress.add_task(f"Downloading {file_name}", total=size)
              async for chunk in resp.content.iter_chunked(4096):
                with open(file_name, 'ab') as f:
                  f.write(chunk)
                progress.update(task,advance=len(chunk))
                await asyncio.sleep(0)
        except ClientConnectionError as e:
           return e
        except ClientConnectorError as e:
            return e
        except TimeoutError as e:
            return e
        except asyncio.CancelledError as e:
            return e
        except Exception as e:
            return e

    async def add_session(self):
           async with aiohttp.ClientSession() as session:
             with Progress() as progress:
              for url in self.parse.add:
                task = asyncio.create_task(self.fetch_data(session,url,progress))
                self.sessions.append(task)
              stop_task = asyncio.create_task(self.fetch_stop())
              Error =  await asyncio.gather(*self.sessions,stop_task,return_exceptions=True)

           if isinstance(Error,list):
               for error in Error:
                   print(error)

    def add_arguments(self):
        self.parser.add_argument("--add", help="add a link", nargs="+", required=True, type=str)
        self.parser.add_argument("--path", help="add a path", required=False, type=str)

ref = CLI_downloder()
start = time.time()
asyncio.run(ref.add_session())
total = time.time() - start
print(total)

