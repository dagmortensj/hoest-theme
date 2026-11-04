# Julia: typer, multippel dispatch, makroer og vektorisering
module Fysikk

using LinearAlgebra
import Base: show, +

export Legeme, kraft

const G = 6.674e-11
abstract type AbstraktLegeme end

struct Legeme{T<:Real} <: AbstraktLegeme
    navn::String
    masse::T
    posisjon::Vector{T}
end

mutable struct Teller
    n::Int
end

"""
    kraft(a, b)

Gravitasjonskraften mellom `a` og `b`.
"""
function kraft(a::Legeme, b::Legeme; ε::Float64=1e-9)::Float64
    r = norm(b.posisjon .- a.posisjon); r += ε
    return G * a.masse * b.masse / r^2
end

show(io::IO, l::Legeme) = print(io, "$(l.navn): $(l.masse) kg\n")
kvadrater = [x^2 for x in 1:10 if iseven(x)]; kvadrater .+= 1
@time sum(sin.(range(0, 2π, length=100)))
x = 2.5im; y = true ? nothing : missing; z = :symbol
end # module

# Vanskelige tilfeller: operatoroverlasting, kringkasting, makroer, strenger og typer
import Base: *, ==
struct Vektor{T<:Real} <: AbstractVector{T}
    x::T; y::T
end
+(a::Vektor, b::Vektor) = Vektor(a.x + b.x, a.y + b.y)
*(k::Real, v::Vektor) = Vektor(k * v.x, k * v.y)
==(a::Vektor, b::Vektor) = a.x == b.x && a.y == b.y
Base.getindex(v::Vektor, i::Int) = i == 1 ? v.x : v.y
Base.size(::Vektor) = (2,)
macro tid(uttrykk) return :(@elapsed $(esc(uttrykk))) end
function vanskelig(navn::Union{String,Nothing}=nothing, verdier::Vector{Int}=Int[]; nøkkel=1, resten...)::Int
    t = 0; t += 1; t -= 2; t *= 3; t ÷= 4; t %= 5; t ^= 2; t <<= 1; t |= 1; t ⊻= 2; t &= ~3; t //= 1
    lik = t == 1 || t === 1 && t != nothing && !(t < 2) || 0 ≤ t ≤ 2 ≠ 1; neg = -t + +t % 2^3
    v = Vektor(1, 2) + 2 * Vektor(3, 4); lik &= v == v && v[1] != v[2]; w = [1, 2] .+ [3, 4] .* 2 .^ 2
    w .+= 1; w .*= 2; w .= 0; w[end] = w[begin] + length(w) ÷ 2
    tekst = "a + b == c $(navn) $t \t\u00e6" * raw"rå \n $x" * """
        flere linjer
        """
    for i in 1:2:10, j in 1:i if i % 3 == 0 || i ∈ verdier continue elseif i ∉ 3:7 break end end
    resultat = if t < 0 -t elseif 1 <= t <= 9 nøkkel else something(get(resten, :x, nothing), 0) end
    return sum(x -> x^2, verdier; init=0) + resultat + length(tekst) + Int(lik) + neg + (sum(w) |> round |> Int)
end
