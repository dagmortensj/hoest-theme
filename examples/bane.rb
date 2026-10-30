# Eksempelfil for å se Høst-temaene på Ruby.
require "json"

module Fysikk
  G = 6.674e-11

  class Legeme
    attr_reader :navn, :masse

    def initialize(navn, masse, posisjon = [0.0, 0.0])
      @navn = navn
      @masse = masse
      @posisjon = posisjon
    end

    def kraft(annet)
      dx, dy = annet.posisjon.zip(@posisjon).map { |a, b| a - b }
      r = Math.hypot(dx, dy)
      raise ArgumentError, "Kollisjon mellom #{navn} og #{annet.navn}\n" if r.zero?

      G * masse * annet.masse / r**2
    end

    def to_s = "#<Legeme #{@navn}>"

    protected

    attr_reader :posisjon
  end
end

sola = Fysikk::Legeme.new("Sola", 1.989e30)
3.times do |i|
  puts "Steg #{i}: #{sola}" unless sola.nil?
end
puts({ navn: sola.navn, aktiv: true }.to_json)
