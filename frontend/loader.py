from aiogram.utils.markdown import hbold

greeting = (
    "Привет! Я телеграм бот для отслеживания привычек. "
    "Я помогу вам избавиться от ненужных и выработать новые. "
    "Чтобы узнать как пользоваться ботом, в меню бота выберите пункт "
    "как пользоваться ботом."
)


guide = (
    "Для работы с ботом первое что нужно сделать, это зарегистрироваться. "
    "Для регистрации используется ваш username телеграмм, а также идентификатор"
    " чата. Все что вам нужно будет ввести это ваш пароль. Пожалуйста запомните "
    "его, функции восстановить пароль пока не предусмотрено. При входе в ваш "
    "аккаунт вам будет выдаваться токен(под капотом), который будет "
    "действительным в течении недели, затем нужно будет войти заново."
    "Для добавления привычки вам нужно будет сначала ввести Название привычки, "
    "затем подробное описание для чего вам это нужно или какие цели вы "
    "достигнете если приобретете новую привычку, а затем количество дней для "
    "отслеживания(рекомендация для приобретения новой привычки не менее 21 дня)."
    "Так же не следует пытаться приобрести много новых привычек сразу, лучше "
    "не более трех за раз, так как это достаточно серьезное испытание для "
    "вашего организма. Далее вам требуется ежедневно делать отметки о "
    "выполнении/невыполнении привычки за определенный день. Если вы отметили "
    "привычку как невыполненную вам к вашему количеству дней выполнения "
    "прибавиться день. Если количество отметок о невыполнении превысит три, "
    "то все отметки автоматически удаляться, и вам нужно будет все начинать "
    "сначала. Чтобы не забыть отметить выполнение/невыполнение рекомендуется "
    "добавить напоминание в удобный для вас час. Когда количество успешных "
    "отметок будет соответствовать вашему количеству дней для отслеживания, "
    "привычка автоматически переместиться в архив."
)


enter_email: str = hbold("Введите ваш email.")

password: str = (hbold('Введите пароль.')  +
                 "\nПароль должен быть не короче 5 символов и содержать "
                 "буквы и цифры.")

success_registration: str = ("Вы успешно зарегистрировались! Теперь вы имеете "
                             "доступ к остальному функционалу бота.")

success_auth: str = "Вы авторизованы."

mark_as_archive: str = ("Привычка будет помечена как архивная и не "
                        "будет отображаться в активных привычках. \nНажмите "
                        "да чтобы продолжить или нет чтобы отменить действие.")

archived: str = ("Привычка была помечена как выполнена и не "
                 "будет отображаться в списке активных привычек.")

not_auth: str = ("Вы не авторизованы. Пройдите процесс регистрации если вы "
                "не зарегистрированы или процесс аутентификации если вы уже "
                 "проходили регистрацию.")

delete_habit_message: str = ("Привычка будет удалена без возможности восстановления, "
                     " чтобы продолжить нажмите да.")

success_save: str = ("Ваша привычка успешно сохранена. Не забывайте "
                     "ежедневно выполнять ее и добавлять в отслеживание.")

update_data: str = ("Ваша привычка успешно обновлена. Не забывайте ежедневно "
                    "выполнять ее и добавлять в отслеживание.")
