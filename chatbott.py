import os
import openai
import sys
from rich import print
from rich.console import Console
from rich.text import Text
openai.organization = "org-P2NXGLnMMliHejCMU7yPAOPL"
openai.api_key = os.getenv('OPENAI_API_KEY')
# openai.Model.list()
# openai.Model.retrieve("text-davinci-003")
# openai.Engine.list()
# openai.Engine.retrieve("davinci")
os.system('pause')


console = Console()
opening = Text.from_markup(
    f"which function do you want to use? [bold italic magenta](1.chat 2.translate 3.edit)[/bold italic magenta]\nplease enter the number:")
print(opening)
num = input()
totalTokens = 0
maxTokens = 4096


class GPT3:

    def fnum(num, recur):
        if num == '1':
            print(Text.from_markup(
                f"[bold italic cyan]you have chosen chat function, let's pop up![/bold italic cyan] > "))
            prompt = ''
            text = ''
            GPT3.gpt_turbo_chat(prompt, text, num, totalTokens, maxTokens)
        elif num == '2' or num == '3':
            GPT3.recall(num, recur, totalTokens, maxTokens)
        elif num == 'quit':
            print(Text.from_markup(
                f"[bold italic red]you have chosen to quit, bye![/bold italic red]"))
            sys.exit()
        else:
            print(Text.from_markup(
                f"[bold italic red]please enter the correct number![/bold italic red]"))
            print(opening)
            num = input()
            GPT3.fnum(num, recur=False)

    def response(messages, totalTokens, maxTokens):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            # [m['content'] for m in messages if m["role"] == "user"],
            presence_penalty=1,
            frequency_penalty=1,
            temperature=0.3,
            # stream=True,
            n=1,
            user="spikezz"
        )
        totalTokens += response["usage"]["total_tokens"]
        message = response["choices"][0]['message']['content']
        ans = Text.from_markup(
            f"[bold green]ChatGPT: {message.strip()}[/bold green]")
        print(ans)
        messages.append({
            "role": "assistant",
            "content": message,
        })

    def dcall(prompt, num, totalTokens, maxTokens, textori):
        messages = [{"role": "system", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            # [m['content'] for m in messages if m["role"] == "user"],
            presence_penalty=0.5,
            frequency_penalty=1,
            temperature=0.3,
            # stream=True,
            n=1,
            user="spikezz"
        )
        totalTokens += response["usage"]["total_tokens"]
        message = response["choices"][0]['message']['content']
        ans = Text.from_markup(
            f"[bold green]ChatGPT: {message.strip()}[/bold green]")
        print(ans)
        messages.append({"role": "assistant", "content": message})
        if num == '2':
            msg = input(
                f"context you want to translate > ")
            if msg == 'change lang':
                translan = input(
                    f"which language do you want to translate to? > ")
                changedPrompt = f"translate {textori} to {translan} as precisely as possible"
                GPT3.dcall(changedPrompt, num, totalTokens, maxTokens, textori)
            elif msg == 'reset':
                GPT3.fnum(num, recur=True)
        elif num == '3':
            msg = input(
                f"sentence or paragraph you want to edit > ")
            if msg == 'change lang':
                editlan = input(
                    f"which language do you want to edit to? > ")
                changedPrompt = f"{textori} Fix the spelling mistakes and polish it elegantly in {editlan}"
                GPT3.dcall(changedPrompt, num, totalTokens, maxTokens, textori)
            elif msg == 'reset':
                GPT3.fnum(num, recur=True)
            else:
                return GPT3.gpt_turbo_chat(prompt, num, totalTokens, maxTokens)

    def recall(num, recur, totalTokens, maxTokens):
        if num == '2':
            if recur:
                text = input(
                    f"context you want to translate > ")
                GPT3.logi(text, num, totalTokens, maxTokens)
                translan = input(
                    f"which language do you want to translate to? > ")
                GPT3.logi(translan, num, totalTokens, maxTokens)
                prompt = f"translate {text}to + {translan} as precisely as possible"
                GPT3.gpt_turbo_chat(prompt, text, num, totalTokens, maxTokens)
            elif not recur:
                print(Text.from_markup(
                    f"[bold italic cyan]you have chosen translate function, let's get start![/bold italic cyan]"))
                text = input(
                    f'context you want to translate > ')
                GPT3.logi(text, num, totalTokens, maxTokens)
                translan = input(
                    f"which language do you want to translate to? > ")
                GPT3.logi(translan, num, totalTokens, maxTokens)
                prompt = f"translate {text}to + {translan} as precisely as possible"
                GPT3.gpt_turbo_chat(prompt, text, num, totalTokens, maxTokens)
        if num == '3':
            if recur:
                text = input(
                    f'sentence or paragraph you want to edit > ')
                editlan = input(f'which language do you want to edit to? > ')
                GPT3.logi(editlan, num, totalTokens, maxTokens)
                prompt = f"{text} Fix the spelling mistakes and polish it elegantly in {editlan}"
                GPT3.gpt_turbo_chat(prompt, text, num, totalTokens, maxTokens)
            elif not recur:
                print(Text.from_markup(
                    f"[bold italic cyan]you have chosen edit function, just gimme your phrases![/bold italic cyan]"))
                text = input(
                    f'sentence or paragraph you want to edit > ')
                editlan = input(f'which language do you want to edit to? > ')
                GPT3.logi(editlan, num, totalTokens, maxTokens)
                prompt = f"{text} Fix the spelling mistakes and polish it elegantly in {editlan}"
                GPT3.gpt_turbo_chat(prompt, text, num, totalTokens, maxTokens)

    def logi(msg, numm, totalTokens, maxTokens):
        if msg:
            if msg == 'quit':
                print(Text.from_markup(
                    f"[bold italic red]you have chosen to quit, bye![/bold italic red]"))
                sys.exit()
            if msg == 'exit':
                print(opening)
                num = input()
                GPT3.fnum(num, recur=True)
            if msg == 'reset' and (numm == '2' or numm == '3'):
                GPT3.fnum(numm, recur=True)
            else:
                return msg, numm, totalTokens, maxTokens
        else:
            if numm == '1':
                msg2 = input(
                    f"please enter something to chat > ")
                msg = msg2
                if msg2:
                    return msg, numm, totalTokens, maxTokens
                while not msg2:
                    msg3 = input(
                        'Do you want to back to menu? Y/N > ')
                    if msg3 == 'Y' or msg3 == 'y':
                        print(opening)
                        num = input()
                        GPT3.fnum(num, recur=True)
                    else:
                        continue
            elif numm == '2':
                msg2 = input(
                    f"please enter something to translate > ")
                msg = msg2
                if msg2:
                    return msg, numm, totalTokens, maxTokens
                while not msg2:
                    msg3 = input(
                        'Do you want to back to menu? Y/N > ')
                    if msg3 == 'Y' or msg3 == 'y':
                        print(opening)
                        num = input()
                        GPT3.fnum(num, recur=True)
                    else:
                        continue
            elif numm == '3':
                msg2 = input(
                    f"please enter something to edit > ")
                msg = msg2
                if msg2:
                    return msg, numm, totalTokens, maxTokens
                while not msg2:
                    msg3 = input(
                        'Do you want to back to menu? Y/N > ')
                    if msg3 == 'Y' or msg3 == 'y':
                        print(opening)
                        num = input()
                        GPT3.fnum(num, recur=True)
                    else:
                        continue

    def gpt_turbo_chat(prompt, text, num, totalTokens, maxTokens):
        if num == '1':
            messages = [{"role": "system",
                         "content": "You are ChatGPT, a large language model trained by OpenAI. reply as precisely as possible"}]
            text = input(
                f"what do you want to say to ChatGPT > ")
        else:
            messages = [{"role": "system", "content": prompt}]
        GPT3.logi(text, num, totalTokens, maxTokens)
        messages.append({"role": "user", "content": text})
        GPT3.response(messages, totalTokens, maxTokens)

        while True:
            if num == '1':
                messages = [{"role": "system",
                             "content": "You are ChatGPT, a large language model trained by OpenAI. reply as precisely as possible"}]
                msg = input(
                    f"what do you want to say to ChatGPT > ")
                GPT3.logi(msg, num, totalTokens, maxTokens)
                messages.append({"role": "user", "content": msg})
                GPT3.response(messages, totalTokens, maxTokens)
            if num == '2':
                messages = [{"role": "system", "content": prompt}]
                msg = input(
                    f"context you want to translate > ")
                if msg == 'change lang':
                    translan = input(
                        f"which language do you want to translate to? > ")
                    changedPrompt = f"translate {text} to {translan} as precisely as possible"
                    GPT3.dcall(changedPrompt, num, totalTokens,
                               maxTokens, textori=text)
                else:
                    GPT3.logi(msg, num, totalTokens, maxTokens)
                    messages.append({"role": "user", "content": msg})
                    GPT3.response(messages,
                                  totalTokens, maxTokens)
            elif num == '3':
                messages = [{"role": "system", "content": prompt}]
                msg = input(
                    f'sentence or paragraph you want to edit > ')

                if msg == 'change lang':
                    editlan = input(
                        f'which language do you want to edit to? > ')
                    changedPrompt = f"{text} Fix the spelling mistakes and polish it elegantly in {editlan}"
                    GPT3.dcall(changedPrompt, num, totalTokens,
                               maxTokens, textori=text)
                else:
                    GPT3.logi(msg, num, totalTokens, maxTokens)
                    messages.append({"role": "user", "content": msg})
                    GPT3.response(messages, totalTokens, maxTokens)


GPT3.fnum(num, recur=False)
