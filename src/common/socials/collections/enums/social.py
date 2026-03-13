import enum


class Social(enum.StrEnum):
    # Основные социальные сети
    vk = "vk"
    ok = "ok"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    telegram = "telegram"
    whatsapp = "whatsapp"
    tiktok = "tiktok"
    snapchat = "snapchat"
    pinterest = "pinterest"
    reddit = "reddit"
    discord = "discord"
    clubhouse = "clubhouse"
    threads = "threads"

    # Видео и стриминг
    youtube = "youtube"
    twitch = "twitch"
    vimeo = "vimeo"
    rutube = "rutube"

    # Профессиональные сети
    linkedin = "linkedin"
    xing = "xing"
    viadeo = "viadeo"

    # Для разработчиков
    github = "github"
    gitlab = "gitlab"
    bitbucket = "bitbucket"
    stackoverflow = "stackoverflow"
    dev_to = "dev_to"
    codepen = "codepen"
    codesandbox = "codesandbox"
    hackerrank = "hackerrank"
    leetcode = "leetcode"
    kaggle = "kaggle"

    # Для дизайнеров и творческих профессий
    behance = "behance"
    dribbble = "dribbble"
    artstation = "artstation"
    soundcloud = "soundcloud"
    bandcamp = "bandcamp"
    vsco = "vsco"
    medium = "medium"
    substack = "substack"

    # Фриланс и карьера
    upwork = "upwork"
    freelancer = "freelancer"
    fiverr = "fiverr"
    toptal = "toptal"
    guru = "guru"
    glassdoor = "glassdoor"
    indeed = "indeed"
    headhunter = "headhunter"
    superjob = "superjob"
    rabota_ru = "rabota_ru"

    # Академические и научные
    researchgate = "researchgate"
    academia_edu = "academia_edu"
    orcid = "orcid"
    scholar = "scholar"
    mendeley = "mendeley"

    # Бизнес и стартапы
    crunchbase = "crunchbase"
    angel_list = "angel_list"
    product_hunt = "product_hunt"
    figma = "figma"
    notion = "notion"

    # Мессенджеры и коммуникация
    slack = "slack"
    microsoft_teams = "microsoft_teams"
    skype = "skype"
    zoom = "zoom"
    signal = "signal"

    avito = "avito"

    # Общие
    website = "website"
    blog = "blog"
    email = "email"
    phone = "phone"
