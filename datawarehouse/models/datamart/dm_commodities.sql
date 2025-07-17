
with commodities as (
    select
        data,
        simbolo,
        valor_fechamento
    from 
        {{ ref ('stg_commodities') }}
),

movimentacao as (
    select
        data,
        simbolo,
        acao,
        quantidade
    from 
        {{ ref ('stg_movimentacao_commodities') }}
),

joined as (
    select
        c.data,
        c.simbolo,
        c.valor_fechamento,
        m.acao,
        m.quantidade,
        (m.quantidade * c.valor_fechamento) as valor,
        case
            when m.acao = 'sell' then (m.quantidade * c.valor_fechamento)
            else -(m.quantidade * c.valor_fechamento)
        end as ganho
    from
        commodities c
    inner join
        movimentacao m
    on
        c.data = m.data
        and c.simbolo = m.simbolo
)

select
    data,
    simbolo,
    valor_fechamento,
    acao,
    quantidade,
    valor,
    ganho
from
    joined
order by 
    data, simbolo