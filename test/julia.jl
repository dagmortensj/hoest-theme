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
    r = norm(b.posisjon .- a.posisjon) + ε
    return G * a.masse * b.masse / r^2
end

show(io::IO, l::Legeme) = print(io, "$(l.navn): $(l.masse) kg\n")
kvadrater = [x^2 for x in 1:10 if iseven(x)]
@time sum(sin.(range(0, 2π, length=100)))
x = 2.5im; y = true ? nothing : missing; z = :symbol
end # module
