#ifndef GAIA_SELECTDESC_H
#define GAIA_SELECTDESC_H

#include "applier.h"
#include "utils.h"

namespace gaia2 {

/**
 * @ingroup appliers
 * SelectDesc applier class. Selects specified dimensions from given point.
 */
class SelectDesc : public Applier {
 protected:
  QStringList _select;

 public:
  SelectDesc(const Transformation& transfo);
  virtual ~SelectDesc();

  /**
   * Ownership of resulting point is handed to caller of this function.
   */
  virtual Point* mapPoint(const Point* p) const;

 protected:
  PointLayout mapLayout(const PointLayout& layout) const;
  PointLayout _newLayout;
  IndexMap _realMap, _stringMap, _enumMap;
};

} // namespace gaia2

#endif // GAIA_SELECTDESC_H
