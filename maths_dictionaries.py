from telegram import InlineKeyboardButton

global_spisok_names = ['Тригонометрия', 'Уравнения и неравенства', 'Алгебраические системы', 'Текстовые задачи',
                       'Параметры', 'Планиметрия', 'Стереометрия', 'Из вариантов олимпиад прошлых лет',
                       'Нестандартные задачи']


slovar = {'-TRIGONOMETRY-': ['TRIGONOMETRY_EQUATIONS', 'SQUARE_EQUATIONS', 'SINGLE_TRIGONOMETRY',
                             'TRIGONOMETRY_SYSTEM', 'TRANSFORMATIONS', 'INVERSE_FUNCTIONS', 'SUPPORT_ANGLE'],
          '-EQUATIONS-': ['MODULO_EQUATIONS', 'RATIONAL_EQUATIONS', 'EQUATIONS_WITH_RADICALS', 'EXPONENTIAL_EQUATIONS',
                          'LOGARITHMIC_EQUATIONS', 'MIXED_TRIGONOMETRY', 'MIXED_EQUATIONS'],
          '-SYSTEM-': ['SIMPLE_EQUATION_SYSTEMS', 'SQUARE_EQUATIONS', 'ARISING_FROM_TEXT_TASKS'],
          '-TEXT_TASKS-': ['MOVEMENT_TASKS', 'TASKS_FOR_WORK', 'TASKS_ON_MIXTURES', 'PROGRESSION_TASKS',
                           'OPTIMAL_CHOICE'],
          '-PARAMETERS-': ['SQUARE_EQ_NERVES_PARAMETER', 'LOGICAL_TASKS', 'DIFFICULT_LOG_TASKS',
                           'WITH_ROOTS'],
          '-PLANIMETRY-': ['COMMON_TRIANGLES', 'SEMBLANCE', 'SQUARES',
                           'PARALLEL_TRAPEZOIDS', 'CIRCLES', 'BUILDINGS'],
          '-STEREOMETRY-': [],
          '-OTHER_VAR-': ['PHYSTECH', 'OMMO', 'PVG',
                          'LOMONOSOV', 'ROSATOM', 'SAMMAT', 'GAZPROM'],
          '-NON_STANDART-': ['MAJOR_METHOD', 'FUNCTIONS', 'GROUPING',
                             'GEOMETRIC_APPROACH']
          }


slovar_names = {'-TRIGONOMETRY-': 'Тригонометрия',
                '-EQUATIONS-': 'Уравнения и неравенства',
                '-SYSTEM-': 'Алгебраические системы',
                '-TEXT_TASKS-': 'Текстовые задачи',
                '-PARAMETERS-': 'Параметры',
                '-PLANIMETRY-': 'Планиметрия',
                '-STEREOMETRY-': 'Стереометрия',
                '-OTHER_VAR-': 'Из вариантов олимпиад прошлых лет',
                '-NON_STANDART-': 'Нестандартные задачи'
                }


global_slovar = {'Тригонометрия': [
                              [InlineKeyboardButton("Триг. ур-ия", callback_data='TRIGONOMETRY_EQUATIONS')],
                              [InlineKeyboardButton("Сведение к кв-ым триг. ур-ям",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Однородные ур-ия", callback_data='SINGLE_TRIGONOMETRY')],
                              [InlineKeyboardButton("Системы триг. уравнений", callback_data='TRIGONOMETRY_SYSTEM')],
                              [InlineKeyboardButton("Преобразование триг. уравнений",
                                                    callback_data='TRANSFORMATIONS')],
                              [InlineKeyboardButton("Обратные триг. функции", callback_data='INVERSE_FUNCTIONS')],
                              [InlineKeyboardButton("Метод вспомогательного угла в триг.",
                                                    callback_data='SUPPORT_ANGLE')]],
                 'Уравнения и неравенства': [
                              [InlineKeyboardButton("Уравнения и неравенства с модулем",
                                                    callback_data='MODULO_EQUATIONS')],
                              [InlineKeyboardButton("Рациональные уравнения и неравенства",
                                                    callback_data='RATIONAL_EQUATIONS')],
                              [InlineKeyboardButton("Уравнения и неравенства с радикалами",
                                                    callback_data='EQUATIONS_WITH_RADICALS')],
                              [InlineKeyboardButton("Показательные уравнения", callback_data='EXPONENTIAL_EQUATIONS')],
                              [InlineKeyboardButton("Логарифмические уравнения",
                                                    callback_data='LOGARITHMIC_EQUATIONS')],
                              [InlineKeyboardButton("Смешанная тригонометрия", callback_data='MIXED_TRIGONOMETRY')],
                              [InlineKeyboardButton("Смешанные уравнения",
                                                    callback_data='MIXED_EQUATIONS')]],
                 'Алгебраические системы': [
                              [InlineKeyboardButton("Простые системы уравнений",
                                                    callback_data='SIMPLE_EQUATION_SYSTEMS')],
                              [InlineKeyboardButton("Сложные системы уравнений",
                                                    callback_data='SQUARE_EQUATIONS')],
                              [InlineKeyboardButton("Возникающие из текстовых задач",
                                                    callback_data='ARISING_FROM_TEXT_TASKS')]],

                 'Текстовые задачи': [
                              [InlineKeyboardButton("Задачи на движение", callback_data='MOVEMENT_TASKS')],
                              [InlineKeyboardButton("Задачи на работу",
                                                    callback_data='TASKS_FOR_WORK')],
                              [InlineKeyboardButton("Задачи на смеси", callback_data='TASKS_ON_MIXTURES')],
                              [InlineKeyboardButton("Задачи на прогрессии", callback_data='PROGRESSION_TASKS')],
                              [InlineKeyboardButton("Оптимальный выбор и целые числа",
                                                    callback_data='OPTIMAL_CHOICE')]],

                 'Параметры': [
                              [InlineKeyboardButton("Квадратные ур-ия и нер-ва с параметром",
                                                    callback_data='SQUARE_EQ_NERVES_PARAMETER')],
                              [InlineKeyboardButton("Логические задачи",
                                                    callback_data='LOGICAL_TASKS')],
                              [InlineKeyboardButton("Сложные логические задачи", callback_data='DIFFICULT_LOG_TASKS')],
                              [InlineKeyboardButton("Параметры с корнями", callback_data='WITH_ROOTS')]],

                 'Планиметрия': [
                              [InlineKeyboardButton("Общие треугольники", callback_data='COMMON_TRIANGLES')],
                              [InlineKeyboardButton("Подобие",
                                                    callback_data='SEMBLANCE')],
                              [InlineKeyboardButton("Площади", callback_data='SQUARES')],
                              [InlineKeyboardButton("Параллелограммы и трапеции", callback_data='PARALLEL_TRAPEZOIDS')],
                              [InlineKeyboardButton("Окружности",
                                                    callback_data='CIRCLES')],
                              [InlineKeyboardButton("Построения", callback_data='BUILDINGS')]],

                 'Стереометрия': [],
                 'Из вариантов олимпиад прошлых лет': [
                              [InlineKeyboardButton("Физтех", callback_data='PHYSTECH')],
                              [InlineKeyboardButton("ОММО",
                                                    callback_data='OMMO')],
                              [InlineKeyboardButton("ПВГ", callback_data='PVG')],
                              [InlineKeyboardButton("Ломоносов", callback_data='LOMONOSOV')],
                              [InlineKeyboardButton("Росатом",
                                                    callback_data='ROSATOM')],
                              [InlineKeyboardButton("САММАТ", callback_data='SAMMAT')],
                              [InlineKeyboardButton("Газпром",
                                                    callback_data='GAZPROM')]],

                 'Нестандартные задачи': [
                              [InlineKeyboardButton("Метод мажорант", callback_data='MAJOR_METHOD')],
                              [InlineKeyboardButton("Использование св-в функций",
                                                    callback_data='FUNCTIONS')],
                              [InlineKeyboardButton("Подстановка или группировка",
                                                    callback_data='GROUPING')],
                              [InlineKeyboardButton("Геометрический подход", callback_data='GEOMETRIC_APPROACH')]],

                 }
