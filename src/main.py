import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DEBUG_CONTEXT = False


async def main():
    from consts import TELEGRAM_BOT_TOKEN
    from database.fragments_db import RAGInterface
    from llm.llm_interface import LLMCaller
    from llm.prompt import MAFIA_PROMPT

    rag = RAGInterface()
    llm = LLMCaller(prompt=MAFIA_PROMPT)

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(Command("help"))
    async def help_command(message: Message):
        await message.answer("Это бот для помощи ведущим спортивной мафии в проведении игр. Задайте ему вопрос по теме мафии и он ответит на него, используя турнирные правила ФСМ.")

    @dp.message(F.text)
    async def question_handler(message: Message):
        query = message.text
        results = rag.search_rules(query, k=3)
        context_text = "\n".join(rag.process_fragment(fr) for fr in results)
        print(context_text)
        response = llm.call_model(
            call_params={"query": query,
                         "context": context_text})
        model_answer = llm.get_response_content(response)

        links_pretty = "<b>Релевантные пункты правил ФСМ:</b>\n" + \
            ", ".join([fr['metadata']['paragraph'] for fr in results])
        final_answer = f"{model_answer}\n\n{links_pretty}"

        if DEBUG_CONTEXT:
            context_pretty = "\t • " + "\n\t • ".join(context_text.split("\n"))
            final_answer = f"{model_answer}\n\n<b>Получено на основе фрагментов правил:</b>\n{context_pretty}\n\n{links_pretty}"
        await message.answer(final_answer,
                             parse_mode="HTML")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
